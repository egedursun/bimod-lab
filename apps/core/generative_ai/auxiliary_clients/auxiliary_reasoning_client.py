#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: auxiliary_reasoning_client.py
#  Last Modified: 2024-10-09 00:55:31
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-09 00:55:32
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

from openai import OpenAI

from apps.assistants.utils import (
    MultiStepReasoningCapabilityChoicesNames,
    MultiStepReasoningCapabilityModelNames
)

from apps.core.generative_ai.auxiliary_methods.errors.error_log_prompts import (
    get_no_reasoning_capability_error_log,
    get_default_reasoning_error_log
)

from apps.core.generative_ai.gpt_openai_manager import OpenAIGPTClientManager
from apps.core.generative_ai.utils import ChatRoles

from apps.core.system_prompts.reasoning.reasoning_prompt import (
    build_reasoning_system_prompt
)

logger = logging.getLogger(__name__)


class ReasoningAuxiliaryLLMManager:
    def __init__(
        self,
        assistant,
        chat_object
    ):
        self.connection = OpenAI(
            api_key=assistant.llm_model.api_key
        )
        self.assistant = assistant
        self.chat = chat_object

    def process_reasoning(self, query: str):
        model_name = None

        if self.assistant.multi_step_reasoning_capability_choice == MultiStepReasoningCapabilityChoicesNames.NONE:
            final_output = get_no_reasoning_capability_error_log()
            return final_output

        if self.assistant.multi_step_reasoning_capability_choice == MultiStepReasoningCapabilityChoicesNames.HIGH_PERFORMANCE:
            model_name = MultiStepReasoningCapabilityModelNames.O1_PREVIEW

        elif self.assistant.multi_step_reasoning_capability_choice == MultiStepReasoningCapabilityChoicesNames.COST_EFFECTIVE:
            model_name = MultiStepReasoningCapabilityModelNames.O1_MINI

        if model_name is None:
            final_output = get_no_reasoning_capability_error_log()
            return final_output

        try:

            system_prompt = build_reasoning_system_prompt()
            c = OpenAIGPTClientManager.get_naked_client(
                llm_model=self.assistant.llm_model
            )

            llm_response = c.chat.completions.create(
                model=model_name,
                messages=[
                    {
                        "role": ChatRoles.ASSISTANT,
                        "content": system_prompt
                    },
                    {
                        "role": ChatRoles.USER,
                        "content": query
                    },
                ]
            )

            choices = llm_response.choices
            first_choice = choices[0]
            choice_message = first_choice.message
            choice_message_content = choice_message.content
            final_output = choice_message_content
            logger.info(f"Reasoning response: {final_output}")

        except Exception as e:
            logger.error(f"Failed to reason: {str(e)}")
            final_output = get_default_reasoning_error_log(error_logs=str(e))

        return final_output
