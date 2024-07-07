from apps._services.llms.openai import InternalOpenAIClient
from apps.assistants.models import Assistant
from apps.multimodal_chat.models import MultimodalChat


class InternalLLMClient:

    LLM_CORE_PROVIDERS = {
        "OPENAI": {
            "code": "OA",
            "name": "OpenAI-GPT"
        },
    }

    @staticmethod
    def get(assistant: Assistant, multimodal_chat: MultimodalChat):
        if assistant.llm_model.provider == InternalLLMClient.LLM_CORE_PROVIDERS["OPENAI"]["code"]:
            return InternalOpenAIClient(
                assistant=assistant,
                multimodal_chat=multimodal_chat
            )
