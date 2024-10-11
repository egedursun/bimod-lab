#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: auxiliary_llm_code_analysis_client.py
#  Last Modified: 2024-10-09 01:08:44
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-09 01:08:44
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
import requests
from openai import OpenAI
from openai.types.beta.threads import TextContentBlock, ImageFileContentBlock

from apps.core.generative_ai.auxiliary_methods.affirmations.affirmation_instructions import GENERIC_AFFIRMATION_PROMPT
from apps.core.generative_ai.auxiliary_methods.errors.error_log_prompts import \
    CODE_ANALYST_AGENT_PREPARATION_ERROR_LOG, CODE_ANALYST_THREAD_CREATION_ERROR_LOG, \
    CODE_ANALYST_RESPONSE_RETRIEVAL_ERROR_LOG, CODE_ANALYST_CLEANUP_ERROR_LOG
from apps.core.generative_ai.auxiliary_methods.output_supply_prompts import EMPTY_OBJECT_PATH_LOG, AgentRunConditions
from apps.core.generative_ai.auxiliary_methods.status_logs.status_log_prompts import get_number_of_codes_too_high_log, \
    get_code_interpreter_status_log
from apps.core.generative_ai.auxiliary_methods.tool_helpers.tool_helper_instructions import HELPER_SYSTEM_INSTRUCTIONS
from apps.core.generative_ai.utils import CONCRETE_LIMIT_SINGLE_FILE_INTERPRETATION, ChatRoles, \
    GPT_DEFAULT_ENCODING_ENGINE
from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import LLMTransactionSourcesTypesNames
from config.settings import MEDIA_URL


class AuxiliaryLLMCodeAnalysisManager:

    def __init__(self, assistant, chat_object):
        self.assistant = assistant
        self.chat = chat_object
        self.connection = OpenAI(api_key=assistant.llm_model.api_key)

    def analyze_code_script(self, full_file_paths: list, query_string: str, interpretation_temperature: float):
        c = self.connection
        if len(full_file_paths) > CONCRETE_LIMIT_SINGLE_FILE_INTERPRETATION:
            return get_number_of_codes_too_high_log(max=CONCRETE_LIMIT_SINGLE_FILE_INTERPRETATION), [], []

        f_data = []
        for pth in full_file_paths:
            if not pth:
                return EMPTY_OBJECT_PATH_LOG, [], []
            if not pth.startswith("http"):
                pth = f"{MEDIA_URL}{pth}"
            try:
                f = requests.get(pth)
                f_data.append(f.content)
            except FileNotFoundError:
                continue
            except Exception as e:
                continue

        f_objs = []
        for con in f_data:
            try:
                f = c.files.create(purpose="assistants", file=con)
                f_objs.append(f)
            except Exception as e:
                continue

        try:
            agent = c.beta.assistants.create(
                name=HELPER_SYSTEM_INSTRUCTIONS["code_interpreter"]["name"],
                description=HELPER_SYSTEM_INSTRUCTIONS["code_interpreter"]["description"],
                model="gpt-4o", tools=[{"type": "code_interpreter"}],
                tool_resources={"code_interpreter": {"file_ids": [x.id for x in f_objs]}},
                temperature=float(interpretation_temperature))
        except Exception as e:
            return CODE_ANALYST_AGENT_PREPARATION_ERROR_LOG, [], []

        try:
            thread = c.beta.threads.create(
                messages=[{"role": ChatRoles.USER, "content": (query_string + GENERIC_AFFIRMATION_PROMPT)}])
        except Exception as e:
            return CODE_ANALYST_THREAD_CREATION_ERROR_LOG, [], []

        try:
            run = c.beta.threads.runs.create_and_poll(thread_id=thread.id, assistant_id=agent.id)
        except Exception as e:
            return CODE_ANALYST_RESPONSE_RETRIEVAL_ERROR_LOG, [], []

        txts, img_http_ids, f_http_ids = [], [], []
        if run.status == AgentRunConditions.COMPLETED:
            msgs = c.beta.threads.messages.list(thread_id=thread.id)
            for msg in msgs.data:
                if msg.role == ChatRoles.ASSISTANT:
                    root_content = msg.content
                    for con in root_content:
                        if isinstance(con, TextContentBlock):
                            txt_con = con.text
                            txts.append(txt_con.value)
                            if txt_con.annotations:
                                for annotation in txt_con.annotations:
                                    f_id = annotation.file_path.file_id
                                    f_http_ids.append((f_id, annotation.text))
                        elif isinstance(con, ImageFileContentBlock):
                            img_con = con.image_file.file_id
                            img_http_ids.append(img_con)
        else:
            if run.status == AgentRunConditions.FAILED:
                msgs = get_code_interpreter_status_log(status="failed")
            elif run.status == AgentRunConditions.INCOMPLETE:
                msgs = get_code_interpreter_status_log(status="incomplete")
            elif run.status == AgentRunConditions.EXPIRED:
                msgs = get_code_interpreter_status_log(status="expired")
            elif run.status == AgentRunConditions.CANCELLED:
                msgs = get_code_interpreter_status_log(status="cancelled")
            else:
                msgs = get_code_interpreter_status_log(status="unknown")

        fs_http = []
        for f_id, remote in f_http_ids:
            try:
                data_bytes = c.files.content(f_id).read()
                fs_http.append((data_bytes, remote))
            except Exception as e:
                continue

        imgs_http = []
        for image_id in img_http_ids:
            try:
                data_bytes = c.files.content(image_id).read()
                imgs_http.append(data_bytes)
            except Exception as e:
                continue

        try:
            for f in f_objs:
                try:
                    c.files.delete(f.id)
                except Exception as e:
                    continue
            c.beta.threads.delete(thread.id)
            c.beta.assistants.delete(agent.id)
        except Exception as e:
            return CODE_ANALYST_CLEANUP_ERROR_LOG, [], []

        LLMTransaction.objects.create(
            organization=self.assistant.organization, model=self.assistant.llm_model, responsible_user=None,
            responsible_assistant=self.assistant, encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            transaction_context_content=txts, llm_cost=0, internal_service_cost=0, tax_cost=0, total_cost=0,
            total_billable_cost=0, transaction_type=ChatRoles.ASSISTANT,
            transaction_source=LLMTransactionSourcesTypesNames.GENERATION
        )
        return txts, fs_http, imgs_http
