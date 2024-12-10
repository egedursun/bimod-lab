#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: auxiliary_llm_analyst_client.py
#  Last Modified: 2024-10-09 01:13:21
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-09 01:13:22
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging

import requests
from openai import OpenAI

from openai.types.beta.threads import (
    TextContentBlock,
    ImageFileContentBlock
)

from apps.core.generative_ai.auxiliary_methods.affirmations.affirmation_instructions import (
    GENERIC_AFFIRMATION_PROMPT
)

from apps.core.generative_ai.auxiliary_methods.errors.error_log_prompts import (
    ANALYST_PREPARATION_ERROR_LOG,
    ANALYST_THREAD_CREATION_ERROR_LOG,
    ANALYST_RESPONSE_RETRIEVAL_ERROR_LOG,
    MEDIA_MANAGER_CLEANUP_ERROR_LOG
)

from apps.core.generative_ai.auxiliary_methods.output_supply_prompts import (
    EMPTY_OBJECT_PATH_LOG,
    AgentRunConditions
)

from apps.core.generative_ai.auxiliary_methods.status_logs.status_log_prompts import (
    get_number_of_files_too_high_log,
    get_file_interpreter_status_log
)

from apps.core.generative_ai.auxiliary_methods.tool_helpers.tool_helper_instructions import (
    HELPER_SYSTEM_INSTRUCTIONS
)

from apps.core.generative_ai.utils import (
    CONCRETE_LIMIT_SINGLE_FILE_INTERPRETATION,
    ChatRoles,
    GPT_DEFAULT_ENCODING_ENGINE
)

from apps.llm_transaction.models import LLMTransaction

from apps.llm_transaction.utils import (
    LLMTransactionSourcesTypesNames
)

logger = logging.getLogger(__name__)


class AuxiliaryLLMAnalystClient:

    def __init__(
        self,
        assistant,
        chat_object
    ):
        self.assistant = assistant
        self.chat = chat_object

        self.connection = OpenAI(
            api_key=assistant.llm_model.api_key
        )

    def interrogate_file(
        self,
        full_file_paths: list,
        query_string: str,
        interpretation_temperature: float
    ):

        c = self.connection

        if len(full_file_paths) > CONCRETE_LIMIT_SINGLE_FILE_INTERPRETATION:

            return get_number_of_files_too_high_log(
                max=CONCRETE_LIMIT_SINGLE_FILE_INTERPRETATION
            ), [], []

        contents = []
        for path in full_file_paths:

            if not path:
                return EMPTY_OBJECT_PATH_LOG, [], []

            try:
                f = requests.get(path)
                contents.append(f.content)
                logger.info(f"Retrieved file content from: {path}")

            except FileNotFoundError:
                logger.error(f"File not found at: {path}")
                continue

            except Exception as e:
                logger.error(f"Failed to retrieve file content from: {path}")
                continue

        objects = []
        for data in contents:
            try:
                f = c.files.create(
                    purpose="assistants",
                    file=data
                )

                objects.append(f)

                logger.info(f"Created file object for file content.")

            except Exception as e:
                logger.error(f"Failed to create file object for file content.")
                continue

        try:
            agent = c.beta.assistants.create(
                name=HELPER_SYSTEM_INSTRUCTIONS["file_interpreter"]["name"],
                description=HELPER_SYSTEM_INSTRUCTIONS["file_interpreter"]["description"],
                model="gpt-4o", tools=[
                    {
                        "type": "code_interpreter"
                    }
                ],
                tool_resources={
                    "code_interpreter": {
                        "file_ids": [
                            x.id for x in objects
                        ]
                    }
                },
                temperature=interpretation_temperature,
            )

            logger.info(f"Created new assistant for file interpretation.")

        except Exception as e:
            logger.error(f"Failed to create new assistant for file interpretation.")

            return ANALYST_PREPARATION_ERROR_LOG, [], []

        try:
            thread = c.beta.threads.create(
                messages=[
                    {
                        "role": ChatRoles.USER,
                        "content": (
                            query_string + GENERIC_AFFIRMATION_PROMPT
                        )
                    }
                ]
            )

            logger.info(f"Created new thread for file interpretation.")

        except Exception as e:
            logger.error(f"Failed to create new thread for file interpretation.")

            return ANALYST_THREAD_CREATION_ERROR_LOG, [], []

        try:
            run = c.beta.threads.runs.create_and_poll(
                thread_id=thread.id,
                assistant_id=agent.id
            )

            logger.info(f"Created new run for file interpretation.")

        except Exception as e:
            logger.error(f"Failed to create new run for file interpretation.")

            return ANALYST_RESPONSE_RETRIEVAL_ERROR_LOG, [], []

        txts, img_http_ids, file_http_ids = [], [], []
        if run.status == AgentRunConditions.COMPLETED:

            msgs = c.beta.threads.messages.list(
                thread_id=thread.id
            )

            for msg in msgs.data:
                if msg.role == ChatRoles.ASSISTANT:
                    prime = msg.content

                    for data in prime:

                        if isinstance(data, TextContentBlock):

                            txt_ingredient = data.text
                            txts.append(txt_ingredient.value)

                            if txt_ingredient.annotations:

                                for anno in txt_ingredient.annotations:
                                    f_id = anno.file_path.file_id
                                    file_http_ids.append((f_id, anno.text))
                                pass

                        elif isinstance(data, ImageFileContentBlock):
                            img_data = data.image_file.file_id
                            img_http_ids.append(img_data)

                        else:
                            pass
                    pass
                else:
                    pass
            pass

        else:
            if run.status == AgentRunConditions.FAILED:
                msgs = get_file_interpreter_status_log(
                    status=AgentRunConditions.FAILED
                )

                logger.error(f"File interpretation failed.")

            elif run.status == AgentRunConditions.INCOMPLETE:
                msgs = get_file_interpreter_status_log(
                    status=AgentRunConditions.INCOMPLETE
                )

                logger.error(f"File interpretation incomplete.")

            elif run.status == AgentRunConditions.EXPIRED:
                msgs = get_file_interpreter_status_log(
                    status=AgentRunConditions.EXPIRED
                )

                logger.error(f"File interpretation expired.")

            elif run.status == AgentRunConditions.CANCELLED:
                msgs = get_file_interpreter_status_log(
                    status=AgentRunConditions.CANCELLING
                )

                logger.error(f"File interpretation cancelled.")

            else:
                msgs = get_file_interpreter_status_log(
                    status="unknown"
                )

                logger.error(f"File interpretation status unknown.")

        http_retrieval_files = []

        for f_id, remote in file_http_ids:
            try:
                data_bytes = c.files.content(f_id).read()
                http_retrieval_files.append((data_bytes, remote))
                logger.info(f"Retrieved file content from: {remote}")

            except Exception as e:
                logger.error(f"Failed to retrieve file content from: {remote}")
                continue

        http_retrieval_imgs = []

        for img_id in img_http_ids:
            try:
                data_bytes = c.files.content(img_id).read()
                http_retrieval_imgs.append(data_bytes)

                logger.info(f"Retrieved image content.")

            except Exception as e:
                logger.error(f"Failed to retrieve image content.")
                continue

        try:
            for f in objects:
                try:
                    c.files.delete(f.id)
                    logger.info(f"Deleted file object.")

                except Exception as e:
                    logger.error(f"Failed to delete file object.")
                    continue

            c.beta.threads.delete(thread.id)
            c.beta.assistants.delete(agent.id)

            logger.info(f"Deleted thread and assistant.")

        except Exception as e:
            return MEDIA_MANAGER_CLEANUP_ERROR_LOG, [], []

        LLMTransaction.objects.create(
            organization=self.assistant.organization,
            model=self.assistant.llm_model,
            responsible_user=None,
            responsible_assistant=self.assistant,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            transaction_context_content=txts,
            llm_cost=0,
            internal_service_cost=0,
            tax_cost=0,
            total_cost=0,
            total_billable_cost=0,
            transaction_type=ChatRoles.ASSISTANT,
            transaction_source=LLMTransactionSourcesTypesNames.GENERATION
        )

        logger.info(f"Created new LLM transaction for file interpretation.")

        return txts, http_retrieval_files, http_retrieval_imgs
