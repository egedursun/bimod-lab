#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: llm_decoder.py
#  Last Modified: 2024-09-23 12:33:07
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:07:39
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from apps._services.llms.openai import InternalOpenAIClient
from apps._services.llms.openai_lean import InternalOpenAILeanClient
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
    def get_lean(assistant: Assistant, multimodal_chat: MultimodalChat):
        if assistant.llm_model.provider == InternalLLMClient.LLM_CORE_PROVIDERS["OPENAI"]["code"]:
            print(f"[InternalLLMClient.get_lean] OpenAI provider selected.")
            return InternalOpenAILeanClient(
                assistant=assistant,
                multimodal_chat=multimodal_chat
            )

    @staticmethod
    def provide_analysis(llm_model, statistics):
        if llm_model.provider == InternalLLMClient.LLM_CORE_PROVIDERS["OPENAI"]["code"]:
            print(f"[InternalLLMClient.provide_analysis] OpenAI provider selected.")
            return InternalOpenAIClient.provide_analysis(llm_model=llm_model, statistics=statistics)
        return f"Provider {llm_model.provider} is currently not supported."
