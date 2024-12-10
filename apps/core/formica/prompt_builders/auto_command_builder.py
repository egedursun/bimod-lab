#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: auto_command_builder.py
#  Last Modified: 2024-10-31 05:36:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-02 13:32:48
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

from apps.core.formica.formica_executor_public import (
    FormicaExecutionManager_Public
)

from apps.core.formica.prompts import (
    build_formica_agent_nickname_prompt,
    build_formica_internal_principles_prompt,
    build_formica_agent_personality_prompt,
    build_formica_target_audience_prompt,
    build_formica_user_tenant_prompt,
    build_formica_spatial_awareness_prompt,
    build_formica_technical_dictionary_prompt,
    build_formica_ops_instruction_prompt,
    build_formica_action__auto_prompt_public
)

from apps.core.formica.prompts.formica.whole_text_supplier_prompt import (
    build_whole_text_supply_prompt_public
)

logger = logging.getLogger(__name__)


def build_auto_command_system_prompt_public(
    xc: FormicaExecutionManager_Public,
    content: str
):
    logger.info(f"Building AUTO command system prompt.")

    combined_system_prompt = ""

    generic_instruction_prompt = ""

    generic_instruction_prompt += build_formica_agent_nickname_prompt(
        xc.copilot.name
    )

    generic_instruction_prompt += build_formica_internal_principles_prompt()

    generic_instruction_prompt += build_formica_agent_personality_prompt(
        tone=xc.copilot.tone
    )

    generic_instruction_prompt += build_formica_target_audience_prompt(
        audience=xc.copilot.audience
    )

    generic_instruction_prompt += build_formica_user_tenant_prompt(
        user=xc.copilot.created_by_user
    )

    generic_instruction_prompt += build_formica_spatial_awareness_prompt(
        user=xc.copilot.created_by_user
    )

    generic_instruction_prompt += build_formica_technical_dictionary_prompt(
        glossary=xc.copilot.glossary
    )

    folder_and_doc_info_prompt = build_whole_text_supply_prompt_public(
        content=content
    )

    formica_ops_instruction_prompt = build_formica_ops_instruction_prompt()

    action_instructions_prompt = build_formica_action__auto_prompt_public(
        content=content
    )

    combined_system_prompt += generic_instruction_prompt
    combined_system_prompt += folder_and_doc_info_prompt
    combined_system_prompt += formica_ops_instruction_prompt
    combined_system_prompt += action_instructions_prompt

    return combined_system_prompt
