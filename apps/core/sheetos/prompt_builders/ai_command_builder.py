#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: ai_command_builder.py
#  Last Modified: 2024-10-16 01:31:24
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-16 01:31:25
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

from apps.core.sheetos.prompts import build_sheetos_agent_nickname_prompt, build_sheetos_internal_principles_prompt, \
    build_sheetos_agent_personality_prompt, build_sheetos_target_audience_prompt, build_sheetos_user_tenant_prompt, \
    build_sheetos_spatial_awareness_prompt, build_sheetos_technical_dictionary_prompt, \
    build_sheetos_ops_instruction_prompt, build_sheetos_action__ai_prompt
from apps.core.sheetos.prompts.sheetos.folder_and_document_data_prompt import \
    build_sheetos_folder_and_document_data_prompt
from apps.core.sheetos.prompts.sheetos.whole_text_supplier_prompt import build_whole_text_supply_prompt, \
    build_whole_text_supply_prompt_public
from apps.core.sheetos.sheetos_executor import SheetosExecutionManager

logger = logging.getLogger(__name__)


def build_ai_command_system_prompt(xc: SheetosExecutionManager, user_query: str):
    logger.info(f"Building AI command system prompt for user query: {user_query}")

    combined_system_prompt = ""

    generic_instruction_prompt = ""
    generic_instruction_prompt += build_sheetos_agent_nickname_prompt(
        xc.copilot.name
    )
    generic_instruction_prompt += build_sheetos_internal_principles_prompt()
    generic_instruction_prompt += build_sheetos_agent_personality_prompt(
        tone=xc.copilot.tone
    )
    generic_instruction_prompt += build_sheetos_target_audience_prompt(
        audience=xc.copilot.audience
    )
    generic_instruction_prompt += build_sheetos_user_tenant_prompt(
        user=xc.copilot.created_by_user
    )
    generic_instruction_prompt += build_sheetos_spatial_awareness_prompt(
        user=xc.copilot.created_by_user
    )
    generic_instruction_prompt += build_sheetos_technical_dictionary_prompt(
        glossary=xc.copilot.glossary
    )

    folder_and_doc_info_prompt = build_sheetos_folder_and_document_data_prompt(
        folder=xc.sheetos_document.document_folder,
        doc=xc.sheetos_document
    )
    folder_and_doc_info_prompt += build_whole_text_supply_prompt(
        xc=xc
    )

    sheetos_ops_instruction_prompt = build_sheetos_ops_instruction_prompt()
    action_instructions_prompt = build_sheetos_action__ai_prompt(
        user_query=user_query
    )

    combined_system_prompt += generic_instruction_prompt
    combined_system_prompt += folder_and_doc_info_prompt
    combined_system_prompt += sheetos_ops_instruction_prompt
    combined_system_prompt += action_instructions_prompt
    return combined_system_prompt


def build_ai_command_system_prompt_public(
    xc,
    user_query: str,
    content: str
):
    from apps.core.sheetos.sheetos_executor_public import SheetosExecutionManager_Public
    xc: SheetosExecutionManager_Public

    logger.info(f"Building AI command system prompt for user query: {user_query}")

    combined_system_prompt = ""

    generic_instruction_prompt = ""
    generic_instruction_prompt += build_sheetos_agent_nickname_prompt(
        xc.copilot.name
    )
    generic_instruction_prompt += build_sheetos_internal_principles_prompt()
    generic_instruction_prompt += build_sheetos_agent_personality_prompt(
        tone=xc.copilot.tone
    )
    generic_instruction_prompt += build_sheetos_target_audience_prompt(
        audience=xc.copilot.audience
    )
    generic_instruction_prompt += build_sheetos_user_tenant_prompt(
        user=xc.copilot.created_by_user
    )
    generic_instruction_prompt += build_sheetos_spatial_awareness_prompt(
        user=xc.copilot.created_by_user
    )
    generic_instruction_prompt += build_sheetos_technical_dictionary_prompt(
        glossary=xc.copilot.glossary
    )

    folder_and_doc_info_prompt = build_whole_text_supply_prompt_public(
        content=content
    )

    sheetos_ops_instruction_prompt = build_sheetos_ops_instruction_prompt()
    action_instructions_prompt = build_sheetos_action__ai_prompt(
        user_query=user_query
    )

    combined_system_prompt += generic_instruction_prompt
    combined_system_prompt += folder_and_doc_info_prompt
    combined_system_prompt += sheetos_ops_instruction_prompt
    combined_system_prompt += action_instructions_prompt
    return combined_system_prompt
