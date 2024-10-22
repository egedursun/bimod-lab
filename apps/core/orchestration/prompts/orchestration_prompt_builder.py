#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: orchestration_prompt_builder.py
#  Last Modified: 2024-10-05 02:25:59
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
#
#
import logging

from django.contrib.auth.models import User

from apps.core.orchestration.prompts.orchestration.build_assistant_calls_meta_tool_prompt import \
    build_orchestration_structured_tool_usage_instructions_prompt, build_orchestration_workers_multi_modality_prompt, \
    build_structured_tool_prompt__orchestration_worker_assistant_call_execution
from apps.core.orchestration.prompts.orchestration.build_main_orchestration_prompt import \
    build_structured_orchestrator_primary_guidelines, build_structured_orchestrator_instructions_prompt
from apps.core.system_prompts.agent_configuration.target_audience_prompt_manager import build_target_audience_prompt
from apps.core.system_prompts.agent_configuration.communication_language_prompt_manager import build_communication_language_prompt
from apps.core.system_prompts.agent_configuration.templated_response_prompt_manager import build_templated_response_prompt
from apps.core.system_prompts.agent_configuration.agent_personality_prompt_manager import build_agent_personality_prompt
from apps.core.system_prompts.agent_configuration.communication_user_tenant_prompt_manager import build_user_tenant_prompt
from apps.orchestrations.models import OrchestrationQuery, Maestro


logger = logging.getLogger(__name__)


class OrchestrationPromptBuilder:

    @staticmethod
    def build(query_chat: OrchestrationQuery, maestro: Maestro, user: User, role: str):
        name = maestro.name
        query_chat_text = query_chat.query_text
        response_template = maestro.response_template
        audience = maestro.audience
        tone = maestro.tone
        response_language = maestro.response_language

        ##################################################
        # GENERIC PROMPTS
        primary_guidelines_prompt = build_structured_orchestrator_primary_guidelines()
        structured_instructions_prompt = build_structured_orchestrator_instructions_prompt(maestro=maestro)
        structured_response_template_prompt = build_templated_response_prompt(
            response_template=response_template)
        structured_audience_prompt = build_target_audience_prompt(audience=audience)
        structured_tone_prompt = build_agent_personality_prompt(tone=tone)
        structured_response_language_prompt = build_communication_language_prompt(
            response_language=response_language)
        structured_user_information_prompt = build_user_tenant_prompt(user=user)
        ##################################################
        # MULTI MODALITY PROMPTS
        structured_workers_multi_modality_prompt = build_orchestration_workers_multi_modality_prompt(maestro=maestro)
        ##################################################
        # TOOL PROMPTS
        structured_orchestration_tool_usage_instructions_prompt = build_orchestration_structured_tool_usage_instructions_prompt(
            maestro=maestro)
        structured_orchestration_worker_assistant_call_execution_tool_prompt = (
            build_structured_tool_prompt__orchestration_worker_assistant_call_execution())
        ##################################################

        # Combine the prompts
        merged_prompt = primary_guidelines_prompt
        merged_prompt += structured_instructions_prompt
        merged_prompt += structured_response_template_prompt
        merged_prompt += structured_audience_prompt
        merged_prompt += structured_tone_prompt
        merged_prompt += structured_response_language_prompt
        merged_prompt += structured_user_information_prompt
        ##################################################
        # MULTI MODALITY PROMPTS
        merged_prompt += structured_workers_multi_modality_prompt
        ##################################################
        # GENERIC TOOL PROMPT
        merged_prompt += structured_orchestration_tool_usage_instructions_prompt
        ##################################################
        # SPECIALIZED TOOL PROMPTS
        merged_prompt += structured_orchestration_worker_assistant_call_execution_tool_prompt
        ##################################################

        # Build the dictionary with the role
        prompt = {
            "role": role,
            "content": merged_prompt
        }

        logger.info(f"[OrchestrationPromptBuilder] Built the prompt for the OrchestrationQuery.")
        return prompt
