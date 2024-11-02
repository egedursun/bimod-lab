#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: vect_command_builder.py
#  Last Modified: 2024-10-16 01:32:15
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-16 01:32:15
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

from apps.core.drafting.drafting_executor import DraftingExecutionManager
from apps.core.drafting.drafting_executor_public import DraftingExecutionManager_Public
from apps.core.drafting.prompts import build_drafting_agent_nickname_prompt, build_drafting_internal_principles_prompt, \
    build_drafting_agent_personality_prompt, build_drafting_target_audience_prompt, build_drafting_user_tenant_prompt, \
    build_drafting_spatial_awareness_prompt, build_drafting_technical_dictionary_prompt, \
    build_drafting_ops_instruction_prompt, build_drafting_action__vect_prompt, \
    build_drafting_vector_store_data_source_prompt, build_drafting_tool_prompt__query_vector_store
from apps.core.drafting.prompts.drafting.folder_and_document_data_prompt import \
    build_drafting_folder_and_document_data_prompt
from apps.core.drafting.prompts.drafting.whole_text_supplier_prompt import build_whole_text_supply_prompt, \
    build_whole_text_supply_prompt_public

logger = logging.getLogger(__name__)


def build_vect_command_system_prompt(xc: DraftingExecutionManager, user_query: str):
    logger.info(f"Building VECT command system prompt for user query: {user_query}")

    combined_system_prompt = ""

    generic_instruction_prompt = ""
    generic_instruction_prompt += build_drafting_agent_nickname_prompt(xc.copilot.name)
    generic_instruction_prompt += build_drafting_internal_principles_prompt()
    generic_instruction_prompt += build_drafting_agent_personality_prompt(tone=xc.copilot.tone)
    generic_instruction_prompt += build_drafting_target_audience_prompt(audience=xc.copilot.audience)
    generic_instruction_prompt += build_drafting_user_tenant_prompt(user=xc.copilot.created_by_user)
    generic_instruction_prompt += build_drafting_spatial_awareness_prompt(user=xc.copilot.created_by_user)
    generic_instruction_prompt += build_drafting_technical_dictionary_prompt(glossary=xc.copilot.glossary)

    folder_and_doc_info_prompt = build_drafting_folder_and_document_data_prompt(
        folder=xc.drafting_document.document_folder, doc=xc.drafting_document)
    folder_and_doc_info_prompt += build_whole_text_supply_prompt(xc=xc)

    drafting_ops_instruction_prompt = build_drafting_ops_instruction_prompt()
    action_instructions_prompt = build_drafting_action__vect_prompt(user_query=user_query)

    data_source_prompts = build_drafting_vector_store_data_source_prompt(assistant=xc.copilot)
    tool_execution_prompts = build_drafting_tool_prompt__query_vector_store()

    combined_system_prompt += generic_instruction_prompt
    combined_system_prompt += folder_and_doc_info_prompt
    combined_system_prompt += drafting_ops_instruction_prompt
    combined_system_prompt += action_instructions_prompt

    combined_system_prompt += data_source_prompts
    combined_system_prompt += tool_execution_prompts

    return combined_system_prompt


def build_vect_command_system_prompt_public(xc: DraftingExecutionManager_Public, user_query: str, content: str):
    logger.info(f"Building VECT command system prompt for user query: {user_query}")

    combined_system_prompt = ""

    generic_instruction_prompt = ""
    generic_instruction_prompt += build_drafting_agent_nickname_prompt(xc.copilot.name)
    generic_instruction_prompt += build_drafting_internal_principles_prompt()
    generic_instruction_prompt += build_drafting_agent_personality_prompt(tone=xc.copilot.tone)
    generic_instruction_prompt += build_drafting_target_audience_prompt(audience=xc.copilot.audience)
    generic_instruction_prompt += build_drafting_user_tenant_prompt(user=xc.copilot.created_by_user)
    generic_instruction_prompt += build_drafting_spatial_awareness_prompt(user=xc.copilot.created_by_user)
    generic_instruction_prompt += build_drafting_technical_dictionary_prompt(glossary=xc.copilot.glossary)

    folder_and_doc_info_prompt = build_whole_text_supply_prompt_public(content=content)

    drafting_ops_instruction_prompt = build_drafting_ops_instruction_prompt()
    action_instructions_prompt = build_drafting_action__vect_prompt(user_query=user_query)

    data_source_prompts = build_drafting_vector_store_data_source_prompt(assistant=xc.copilot)
    tool_execution_prompts = build_drafting_tool_prompt__query_vector_store()

    combined_system_prompt += generic_instruction_prompt
    combined_system_prompt += folder_and_doc_info_prompt
    combined_system_prompt += drafting_ops_instruction_prompt
    combined_system_prompt += action_instructions_prompt

    combined_system_prompt += data_source_prompts
    combined_system_prompt += tool_execution_prompts

    return combined_system_prompt
