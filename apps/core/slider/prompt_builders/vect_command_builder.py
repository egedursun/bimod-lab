#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: vect_command_builder.py
#  Last Modified: 2024-11-02 14:57:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-02 21:39:00
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

from apps.core.slider.prompts import (
    build_slider_agent_nickname_prompt,
    build_slider_internal_principles_prompt,
    build_slider_agent_personality_prompt,
    build_slider_target_audience_prompt,
    build_slider_user_tenant_prompt,
    build_slider_spatial_awareness_prompt,
    build_slider_technical_dictionary_prompt,
    build_slider_ops_instruction_prompt,
    build_slider_action__vect_prompt,
)

from apps.core.slider.prompts.slider.whole_text_supplier_prompt import (
    build_whole_text_supply_prompt_public
)

from apps.core.slider.slider_executor_public import (
    SliderExecutionManager_Public
)
from apps.core.system_prompts.information_feeds.vector_store.build_vector_store_data_source_prompt import (
    build_vector_store_data_source_prompt
)

from apps.core.system_prompts.tool_call_prompts.per_tool.execute_vector_store_query_tool_prompt import (
    build_tool_prompt__query_vector_store
)

logger = logging.getLogger(__name__)


def build_vect_command_system_prompt_public(
    xc: SliderExecutionManager_Public,
    user_query: str,
    content: str
):
    logger.info(f"Building VECT command system prompt for user query: {user_query}")

    combined_system_prompt = ""

    generic_instruction_prompt = ""

    generic_instruction_prompt += build_slider_agent_nickname_prompt(
        xc.copilot.name
    )

    generic_instruction_prompt += build_slider_internal_principles_prompt()

    generic_instruction_prompt += build_slider_agent_personality_prompt(
        tone=xc.copilot.tone
    )

    generic_instruction_prompt += build_slider_target_audience_prompt(
        audience=xc.copilot.audience
    )

    generic_instruction_prompt += build_slider_user_tenant_prompt(
        user=xc.copilot.created_by_user
    )

    generic_instruction_prompt += build_slider_spatial_awareness_prompt(
        user=xc.copilot.created_by_user
    )

    generic_instruction_prompt += build_slider_technical_dictionary_prompt(
        glossary=xc.copilot.glossary
    )

    folder_and_doc_info_prompt = build_whole_text_supply_prompt_public(
        content=content
    )

    slider_ops_instruction_prompt = build_slider_ops_instruction_prompt()

    action_instructions_prompt = build_slider_action__vect_prompt(
        user_query=user_query
    )

    data_source_prompts = build_vector_store_data_source_prompt(
        assistant=xc.copilot
    )

    tool_execution_prompts = build_tool_prompt__query_vector_store()

    combined_system_prompt += generic_instruction_prompt
    combined_system_prompt += folder_and_doc_info_prompt
    combined_system_prompt += slider_ops_instruction_prompt
    combined_system_prompt += action_instructions_prompt

    combined_system_prompt += data_source_prompts
    combined_system_prompt += tool_execution_prompts

    return combined_system_prompt
