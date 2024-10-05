#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: audio_processing_executor.py
#  Last Modified: 2024-09-28 22:17:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:35
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: audio_processing_executor.py
#  Last Modified: 2024-09-28 15:44:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:01:09
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from apps._services.config.costs_map import ToolCostsMap
from apps.llm_transaction.utils import TransactionSourcesNames


class AudioProcessingExecutor:

    def __init__(self, assistant, chat):
        from apps._services.llms.openai import InternalOpenAIClient

        self.assistant = assistant
        self.chat = chat
        self.client = InternalOpenAIClient(assistant=self.assistant, multimodal_chat=self.chat)

    def convert_audio_to_text(self, audio_file_path: str):
        from apps.llm_transaction.models import LLMTransaction
        from apps._services.llms.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps._services.llms.utils import ChatRoles

        try:
            transaction = LLMTransaction(
                organization=self.chat.assistant.organization,
                model=self.chat.assistant.llm_model,
                responsible_user=self.chat.user,
                responsible_assistant=self.chat.assistant,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                llm_cost=ToolCostsMap.AudioProcessingSTT.COST,
                transaction_type=ChatRoles.SYSTEM,
                transaction_source=TransactionSourcesNames.AUDIO_PROCESSING_STT,
                is_tool_cost=True
            )
            transaction.save()
        except Exception as e:
            print(f"[BrowsingExecutor.act] Error occurred while creating the transaction: {str(e)}")

        response = self.client.audio_to_text(audio_uri=audio_file_path)
        return response

    def convert_text_to_audio_message(self, message):
        from apps._services.llms.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps._services.llms.utils import ChatRoles
        from apps.llm_transaction.models import LLMTransaction

        try:
            transaction = LLMTransaction(
                organization=self.chat.assistant.organization,
                model=self.chat.assistant.llm_model,
                responsible_user=self.chat.user,
                responsible_assistant=self.chat.assistant,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                llm_cost=ToolCostsMap.AudioProcessingTTS.COST,
                transaction_type=ChatRoles.SYSTEM,
                transaction_source=TransactionSourcesNames.AUDIO_PROCESSING_TTS,
                is_tool_cost=True
            )
            transaction.save()
        except Exception as e:
            print(f"[BrowsingExecutor.act] Error occurred while creating the transaction: {str(e)}")

        response = self.client.text_to_audio_message(message=message)
        return response

    def convert_text_to_audio_file(self, text_content: str, voice_selection: str):
        from apps._services.llms.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps._services.llms.utils import ChatRoles
        from apps.llm_transaction.models import LLMTransaction

        try:
            transaction = LLMTransaction(
                organization=self.chat.assistant.organization,
                model=self.chat.assistant.llm_model,
                responsible_user=self.chat.user,
                responsible_assistant=self.chat.assistant,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                llm_cost=ToolCostsMap.AudioProcessingTTS.COST,
                transaction_type=ChatRoles.SYSTEM,
                transaction_source=TransactionSourcesNames.AUDIO_PROCESSING_TTS,
                is_tool_cost=True
            )
            transaction.save()
        except Exception as e:
            print(f"[BrowsingExecutor.act] Error occurred while creating the transaction: {str(e)}")

        response = self.client.text_to_audio_file(text_content=text_content, voice=voice_selection)
        return response
