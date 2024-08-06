from apps._services.llms.openai import InternalOpenAIClient
from apps.assistants.models import Assistant
from apps.multimodal_chat.models import MultimodalChat


class InternalLLMClient:

    LLM_CORE_PROVIDERS = {
        "OPENAI": {"code": "OA", "name": "OpenAI-GPT"},
    }

    @staticmethod
    def get(assistant: Assistant, multimodal_chat: MultimodalChat):
        if assistant.llm_model.provider == InternalLLMClient.LLM_CORE_PROVIDERS["OPENAI"]["code"]:
            print(f"[InternalLLMClient.get] OpenAI provider selected.")
            return InternalOpenAIClient(
                assistant=assistant,
                multimodal_chat=multimodal_chat
            )

    @staticmethod
    def provide_analysis(llm_model, statistics):
        if llm_model.provider == InternalLLMClient.LLM_CORE_PROVIDERS["OPENAI"]["code"]:
            print(f"[InternalLLMClient.provide_analysis] OpenAI provider selected.")
            return InternalOpenAIClient.provide_analysis(llm_model=llm_model, statistics=statistics)
        return f"Provider {llm_model.provider} is currently not supported."
