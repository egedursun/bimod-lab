#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#
import logging

from apps.core.generative_ai.gpt_openai_manager import OpenAIGPTClientManager
from apps.core.generative_ai.gpt_openai_manager_lean import OpenAIGPTLeanClientManager
from apps.assistants.models import Assistant
from apps.core.generative_ai.statistical_analysis_manager import provide_analysis
from apps.core.generative_ai.utils import LLM_CORE_PROVIDERS
from apps.multimodal_chat.models import MultimodalChat

logger = logging.getLogger(__name__)



class GenerativeAIDecodeController:
    @staticmethod
    def get(assistant: Assistant, multimodal_chat: MultimodalChat):
        if assistant.llm_model.provider == LLM_CORE_PROVIDERS["OPENAI"]["code"]:
            logger.info("OpenAI provider is selected.")
            return OpenAIGPTClientManager(assistant=assistant, chat_object=multimodal_chat)

    @staticmethod
    def get_lean(assistant: Assistant, multimodal_chat: MultimodalChat):
        if assistant.llm_model.provider == LLM_CORE_PROVIDERS["OPENAI"]["code"]:
            logger.info("OpenAI provider is selected.")
            return OpenAIGPTLeanClientManager(assistant=assistant, multimodal_chat=multimodal_chat)

    @staticmethod
    def provide_analysis(llm_model, statistics):
        if llm_model.provider == LLM_CORE_PROVIDERS["OPENAI"]["code"]:
            logger.info("OpenAI provider is selected.")
            return provide_analysis(llm_model=llm_model, statistics=statistics)
        logger.error(f"Provider {llm_model.provider} is not supported by our system to do analysis at the current moment.")
        return f"Provider {llm_model.provider} is not supported by our system to do analysis at the current moment."
