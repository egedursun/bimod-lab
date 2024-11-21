#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: harmoniq_prompt_builder.py
#  Last Modified: 2024-10-11 21:17:49
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-11 21:17:50
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

from apps.core.system_prompts.harmoniq.harmoniq_guidelines_prompt import build_structured_primary_guidelines_harmoniq
from apps.core.system_prompts.harmoniq.harmoniq_instructions_prompt import \
    build_structured_instructions_prompt_harmoniq
from apps.core.system_prompts.harmoniq.harmoniq_name_prompt import build_structured_name_prompt_harmoniq
from apps.core.system_prompts.harmoniq.harmoniq_place_and_time_prompt import \
    build_structured_place_and_time_prompt_harmoniq
from apps.core.system_prompts.harmoniq.multimodality.harmoniq_multimodality_expert_network_prompt import \
    build_expert_networks_multi_modality_prompt_harmoniq
from apps.core.system_prompts.harmoniq.tools.harmoniq_tools_expert_networks_query_prompt import \
    build_structured_tool_prompt__expert_network_query_execution_harmoniq
from apps.core.system_prompts.harmoniq.tools.harmoniq_tools_instructions_prompt import \
    build_structured_tool_usage_instructions_prompt_harmoniq
from apps.harmoniq.models import Harmoniq


logger = logging.getLogger(__name__)


def build_harmoniq_system_prompt(
    harmoniq_agent: Harmoniq,
    expert_net_and_refs: list,
    org_data: dict,
    user_data: dict
):

    logger.info("Building Harmoniq system prompt.")
    system_prompt = ""

    name = build_structured_name_prompt_harmoniq(
        harmoniq=harmoniq_agent
    )
    guidelines = build_structured_primary_guidelines_harmoniq()
    instructions = build_structured_instructions_prompt_harmoniq(
        agent=harmoniq_agent
    )
    spatial_info = build_structured_place_and_time_prompt_harmoniq(
        organization_data=org_data,
        user_data=user_data
    )
    expert_network_prompt = build_expert_networks_multi_modality_prompt_harmoniq(
        expert_net_and_refs=expert_net_and_refs
    )
    tool_instructions = build_structured_tool_usage_instructions_prompt_harmoniq()
    nw_query_instructions = build_structured_tool_prompt__expert_network_query_execution_harmoniq()

    system_prompt += name
    system_prompt += guidelines
    system_prompt += instructions
    system_prompt += spatial_info
    system_prompt += expert_network_prompt
    system_prompt += tool_instructions
    system_prompt += nw_query_instructions

    affirmation_prompt = f"""
        - **DO NOT EXPECT THE USER TO CONFIRM ANYTHING.**
        - If the user tells you to do something JUST DO IT. DO NOT tell about your action plan to them, JUST DO THE
            ACTION FIRST, then tell them what you did.
        - IF YOU AIM TO DO A TOOL CALL, JUST DO IT!!! DON'T TELL THE USER YOU ARE GOING TO DO IT, DON'T ASK FOR THEIR
        APPROVAL, JUST DO IT!!! THEY CAN'T ANSWER YOU.

        ---

        # **LISTEN ""VERY"" CAREFULLY, THIS IS EXTREMELY IMPORTANT:**

            ## DON'T NEGLECT THIS ""EVER"". DONT ASK FOR CONFIRMATION, JUST CALL THE TOOL JSON; JUST CALL THE TOOL
                JSON. JUST CALL THE TOOL JSON, DON'T SAY I WILL DO THAT OR THAT. JUST CALL THE TOOL JSON!!!!

        ---
    """
    system_prompt += affirmation_prompt
    return system_prompt
