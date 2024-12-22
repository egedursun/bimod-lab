#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: ellma_execution_manager.py
#  Last Modified: 2024-10-30 23:18:03
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-30 23:18:03
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

from apps.core.ellma.prompt_builders import (
    build_ellma_transcription_system_prompt
)

from apps.core.generative_ai.gpt_openai_manager import (
    OpenAIGPTClientManager
)

from apps.core.generative_ai.utils import (
    GPT_DEFAULT_ENCODING_ENGINE,
    ChatRoles
)

from apps.ellma.models import EllmaScript

from apps.ellma.utils import (
    EllmaTranscriptionLanguagesNames
)

from apps.llm_core.models import LLMCore
from apps.llm_transaction.models import LLMTransaction

from apps.llm_transaction.utils import (
    LLMTransactionSourcesTypesNames
)

logger = logging.getLogger(__name__)


class EllmaExecutionManager:

    def __init__(self, script: EllmaScript):

        self.script: EllmaScript = script
        self.llm_model: LLMCore = self.script.llm_model

        self.c = OpenAIGPTClientManager.get_naked_client(
            llm_model=self.llm_model
        )

    def transcribe_via_ai(self):

        structured_system_prompt = build_ellma_transcription_system_prompt(
            script=self.script
        )

        raw_code = self.script.ellma_script_content

        context_message_history = [
            {
                "role": ChatRoles.SYSTEM,
                "content": str(structured_system_prompt)
            },
            {
                "role": ChatRoles.USER,
                "content": f"""
                ########################################
                # CONVERT THIS CODE
                ########################################

                {str(raw_code)}

                ########################################
            """
            }
        ]

        try:
            tx = LLMTransaction.objects.create(
                organization=self.script.organization,
                model=self.llm_model,
                responsible_user=self.script.created_by_user,
                responsible_assistant=None,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                transaction_context_content=str(structured_system_prompt),
                llm_cost=0,
                internal_service_cost=0,
                tax_cost=0,
                total_cost=0,
                total_billable_cost=0,
                transaction_type=ChatRoles.SYSTEM,
                transaction_source=LLMTransactionSourcesTypesNames.ELLMA_SCRIPTING
            )

            logger.info(f"[_transcribe_via_ai] Created eLLMa scripting transcription for system prompt.")

        except Exception as e:
            logger.error(
                f"[_transcribe_via_ai] Error creating eLLMa scripting transcription system prompt. Error: {e}")
            pass

        try:
            tx = LLMTransaction.objects.create(
                organization=self.script.organization,
                model=self.llm_model,
                responsible_user=self.script.created_by_user,
                responsible_assistant=None,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                transaction_context_content=str(raw_code),
                llm_cost=0,
                internal_service_cost=0,
                tax_cost=0,
                total_cost=0,
                total_billable_cost=0,
                transaction_type=ChatRoles.USER,
                transaction_source=LLMTransactionSourcesTypesNames.ELLMA_SCRIPTING
            )

            logger.info(f"[_transcribe_via_ai] Created eLLMa scripting transcription for user prompt.")

        except Exception as e:
            logger.error(
                f"[_transcribe_via_ai] Error creating eLLMa scripting transcription for user prompt. Error: {e}")
            pass

        try:
            llm_output = self.c.chat.completions.create(
                model=self.llm_model.model_name,
                messages=context_message_history,
                temperature=int(
                    self.llm_model.temperature
                ),
                max_tokens=int(
                    self.llm_model.maximum_tokens
                )
            )

            logger.info(f"Retrieved eLLMa transcription content")

        except Exception as e:
            logger.error(f"Failed to retrieve eLLMa transcription content: " + str(e))

            return None, "Failed to retrieve eLLMa transcription content: " + str(e)

        try:
            choices = llm_output.choices
            first_choice = choices[0]

            choice_message = first_choice.message
            choice_message_content = choice_message.content
            final_response = choice_message_content

            logger.info(f"Processed eLLMa transcription content.")

        except Exception as e:
            logger.error(f"Failed to eLLMa transcription content: " + str(e))

            return None, "Failed to eLLMa transcription content: " + str(e)

        try:
            tx = LLMTransaction.objects.create(
                organization=self.script.organization,
                model=self.llm_model,
                responsible_user=self.script.created_by_user,
                responsible_assistant=None,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                transaction_context_content=str(choice_message_content),
                llm_cost=0,
                internal_service_cost=0,
                tax_cost=0,
                total_cost=0,
                total_billable_cost=0,
                transaction_type=ChatRoles.ASSISTANT,
                transaction_source=LLMTransactionSourcesTypesNames.ELLMA_SCRIPTING
            )

            logger.info(
                f"[_transcribe_via_ai] Created eLLMa scripting transcription for assistant response (primary).")

        except Exception as e:
            logger.error(
                f"[_transcribe_via_ai] Error creating eLLMa scripting transcription for assistant response (primary). Error: {e}")
            pass

        try:
            for language_name in EllmaTranscriptionLanguagesNames.as_list():
                final_response = final_response.replace(f"```{language_name}", "").replace("```", "")

            final_response = final_response.replace("`", "")

        except Exception as e:
            logger.error(f"Failed to process eLLMa transcription content: " + str(e))

            return None, "Failed to process eLLMa transcription content: " + str(e)

        logger.info(f"Final eLLMa transcription content is retrieved well.")

        return final_response, None
