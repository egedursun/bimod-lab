#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: hadron_node_prompt_builder.py
#  Last Modified: 2024-10-17 22:45:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 22:45:59
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

from apps.core.hadron_prime.prompts import (
    build_core_instructions_prompt,
    build_optional_instructions_prompt,
    build_system_metadata_prompt,
    build_node_metadata_prompt,
    build_hadron_prime_structured_tool_usage_instructions_prompt,
    build_hadron_prime_structured_tool_prompt__expert_network_query_execution,
    build_hadron_prime_expert_networks_multi_modality_prompt
)

from apps.hadron_prime.models import HadronNode

logger = logging.getLogger(__name__)


def build_hadron_prime_system_prompt(
    node: HadronNode,
    current_state: str,
    goal_state: str,
    error_calculation: str,
    measurements: str,
    topic_messages: str,
    sease_logs: str,
    publish_history_logs: str,
    analytical_data: str,
    action_set_data
) -> str:
    combined_system_prompt = ""

    combined_system_prompt += build_core_instructions_prompt()
    combined_system_prompt += build_optional_instructions_prompt(node=node)
    combined_system_prompt += build_system_metadata_prompt(node=node)
    combined_system_prompt += build_node_metadata_prompt(node=node)
    combined_system_prompt += f"""
        ------------------------------------------
        **DATA DECISION INFORMATION FOR EXECUTION BELOW:
        ------------------------------------------

    """
    combined_system_prompt += current_state
    combined_system_prompt += goal_state
    combined_system_prompt += error_calculation
    combined_system_prompt += measurements
    combined_system_prompt += topic_messages
    combined_system_prompt += sease_logs
    combined_system_prompt += publish_history_logs
    combined_system_prompt += analytical_data
    combined_system_prompt += action_set_data

    combined_system_prompt += f"""

        ------------------------------------------
        **END OF DATA DECISION INFORMATION FOR EXECUTION
        ------------------------------------------

        ------------------------------------------
        **START OF MULTI-MODALITY PROMPTS
        ------------------------------------------

    """

    combined_system_prompt += build_hadron_prime_expert_networks_multi_modality_prompt(node=node)
    combined_system_prompt += build_hadron_prime_structured_tool_usage_instructions_prompt()
    combined_system_prompt += build_hadron_prime_structured_tool_prompt__expert_network_query_execution()

    logger.info(f"Combined System Prompt is successfully built for the Hadron Prime System.")
    return combined_system_prompt
