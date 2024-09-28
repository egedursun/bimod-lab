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
