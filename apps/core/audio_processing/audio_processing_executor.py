#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: audio_processing_executor.py
#  Last Modified: 2024-10-05 02:13:34
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:36
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

from apps.core.internal_cost_manager.costs_map import InternalServiceCosts
from apps.llm_transaction.utils import LLMTransactionSourcesTypesNames


logger = logging.getLogger(__name__)


class AudioProcessingExecutor:
    def __init__(
        self,
        assistant,
        chat
    ):
        from apps.core.generative_ai.auxiliary_clients.auxiliary_llm_audio_client import AuxiliaryLLMAudioClient

        self.assistant = assistant
        self.chat = chat
        self.client = AuxiliaryLLMAudioClient(
            assistant=self.assistant,
            chat_object=self.chat
        )

    def convert_audio_to_text(self, audio_file_path: str):

        from apps.llm_transaction.models import LLMTransaction
        from apps.core.generative_ai.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps.core.generative_ai.utils import ChatRoles

        try:
            tx = LLMTransaction(
                organization=self.chat.assistant.organization,
                model=self.chat.assistant.llm_model,
                responsible_user=self.chat.user,
                responsible_assistant=self.chat.assistant,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                llm_cost=InternalServiceCosts.AudioProcessingSTT.COST,
                transaction_type=ChatRoles.SYSTEM,
                transaction_source=LLMTransactionSourcesTypesNames.AUDIO_PROCESSING_STT,
                is_tool_cost=True
            )
            tx.save()
        except Exception as e:
            logger.error(f"Error while saving LLM Transaction: {str(e)}")
            pass

        logger.info(f"Converting audio to text: {audio_file_path}")
        output = self.client.transform_speech_to_text(audio_uri=audio_file_path)

        return output

    def convert_text_to_audio_message(self, message):

        from apps.core.generative_ai.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps.core.generative_ai.utils import ChatRoles
        from apps.llm_transaction.models import LLMTransaction

        try:
            tx = LLMTransaction(
                organization=self.chat.assistant.organization,
                model=self.chat.assistant.llm_model,
                responsible_user=self.chat.user,
                responsible_assistant=self.chat.assistant,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                llm_cost=InternalServiceCosts.AudioProcessingTTS.COST,
                transaction_type=ChatRoles.SYSTEM,
                transaction_source=LLMTransactionSourcesTypesNames.AUDIO_PROCESSING_TTS,
                is_tool_cost=True
            )
            tx.save()
        except Exception as e:
            logger.error(f"Error while saving LLM Transaction: {str(e)}")
            pass

        logger.info(f"Converting text to audio message: {message}")
        output = self.client.tts_audio_content_message(
            message=message
        )

        return output

    def convert_text_to_audio_file(self, text_content: str, voice_selection: str):
        from apps.core.generative_ai.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps.core.generative_ai.utils import ChatRoles
        from apps.llm_transaction.models import LLMTransaction

        try:
            tx = LLMTransaction(
                organization=self.chat.assistant.organization,
                model=self.chat.assistant.llm_model,
                responsible_user=self.chat.user,
                responsible_assistant=self.chat.assistant,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                llm_cost=InternalServiceCosts.AudioProcessingTTS.COST,
                transaction_type=ChatRoles.SYSTEM,
                transaction_source=LLMTransactionSourcesTypesNames.AUDIO_PROCESSING_TTS,
                is_tool_cost=True
            )
            tx.save()

        except Exception as e:
            logger.error(f"Error while saving LLM Transaction: {str(e)}")
            pass

        logger.info(f"Converting text to audio file: {text_content}")
        output = self.client.transform_text_to_speech(
            text_content=text_content,
            voice=voice_selection
        )

        return output
