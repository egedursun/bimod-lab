#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: auxiliary_llm_vision_client.py
#  Last Modified: 2024-10-09 01:13:04
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-09 01:13:23
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#

import base64 as b64

import requests
from openai import OpenAI

from apps.core.generative_ai.auxiliary_methods.affirmations.affirmation_instructions import GENERIC_AFFIRMATION_PROMPT
from apps.core.generative_ai.auxiliary_methods.errors.error_log_prompts import \
    IMAGE_ANALYST_RESPONSE_RETRIEVAL_ERROR_LOG, IMAGE_ANALYST_RESPONSE_PROCESSING_ERROR_LOG
from apps.core.generative_ai.auxiliary_methods.output_supply_prompts import EMPTY_OBJECT_PATH_LOG
from apps.core.generative_ai.auxiliary_methods.status_logs.status_log_prompts import get_number_of_files_too_high_log
from apps.core.generative_ai.auxiliary_methods.tool_helpers.tool_helper_instructions import HELPER_SYSTEM_INSTRUCTIONS
from apps.core.generative_ai.utils import CONCRETE_LIMIT_SINGLE_FILE_INTERPRETATION, ChatRoles, \
    GPT_DEFAULT_ENCODING_ENGINE
from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import LLMTransactionSourcesTypesNames


class AuxiliaryLLMVisionClient:

    def __init__(self, assistant, chat_object):
        self.assistant = assistant
        self.chat = chat_object
        self.connection = OpenAI(api_key=assistant.llm_model.api_key)

    def interpret_image_content(self, full_image_paths: list, query_string: str, interpretation_temperature: float,
                                interpretation_maximum_tokens: int):
        c = self.connection
        if len(full_image_paths) > CONCRETE_LIMIT_SINGLE_FILE_INTERPRETATION:
            return get_number_of_files_too_high_log(max=CONCRETE_LIMIT_SINGLE_FILE_INTERPRETATION)

        img_data = []
        for pth in full_image_paths:
            if not pth:
                return EMPTY_OBJECT_PATH_LOG
            try:
                file = requests.get(pth)
                img_data.append({"binary": file.content, "extension": pth.split(".")[-1]})
            except FileNotFoundError:
                continue
            except Exception as e:
                continue

        img_objs = []
        for image_content in img_data:
            binary = image_content["binary"]
            extension = image_content["extension"]
            image_base64 = b64.b64encode(binary).decode("utf-8")
            img_objs.append({"base64": image_base64, "extension": extension})

        msgs = [
            {"role": ChatRoles.SYSTEM,
             "content": [{"type": "text", "text": HELPER_SYSTEM_INSTRUCTIONS["image_interpreter"]["description"]}]},
            {"role": ChatRoles.USER,
             "content": [{"type": "text", "text": (query_string + GENERIC_AFFIRMATION_PROMPT)}]}
        ]
        for image_object in img_objs:
            formatted_uri = f"data:image/{image_object['extension']};base64,{image_object['base64']}"
            msgs[-1]["content"].append({"type": "image_url", "image_url": {"url": formatted_uri}})

        try:
            llm_output = c.chat.completions.create(
                model=HELPER_SYSTEM_INSTRUCTIONS["image_interpreter"]["model"], messages=msgs,
                temperature=interpretation_temperature, max_tokens=interpretation_maximum_tokens)
        except Exception as e:
            return IMAGE_ANALYST_RESPONSE_RETRIEVAL_ERROR_LOG

        try:
            choices = llm_output.choices
            first_choice = choices[0]
            choice_message = first_choice.message
            choice_message_content = choice_message.content
            final_response = choice_message_content
        except Exception as e:
            return IMAGE_ANALYST_RESPONSE_PROCESSING_ERROR_LOG

        LLMTransaction.objects.create(
            organization=self.assistant.organization, model=self.assistant.llm_model, responsible_user=None,
            responsible_assistant=self.assistant, encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            transaction_context_content=final_response, llm_cost=0, internal_service_cost=0,
            tax_cost=0, total_cost=0, total_billable_cost=0, transaction_type=ChatRoles.ASSISTANT,
            transaction_source=LLMTransactionSourcesTypesNames.GENERATION)
        return final_response
