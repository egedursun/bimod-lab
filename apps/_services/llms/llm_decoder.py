#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: llm_decoder.py
#  Last Modified: 2024-10-05 02:20:19
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:35
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#

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
