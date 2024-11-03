#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: auto_command_builder.py
#  Last Modified: 2024-11-02 14:57:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-02 21:34:42
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

from apps.core.slider.prompts import build_slider_agent_nickname_prompt, build_slider_internal_principles_prompt, \
    build_slider_agent_personality_prompt, build_slider_target_audience_prompt, build_slider_user_tenant_prompt, \
    build_slider_spatial_awareness_prompt, build_slider_technical_dictionary_prompt, \
    build_slider_ops_instruction_prompt, build_slider_action__auto_prompt_public, build_slider_action__auto_prompt
from apps.core.slider.prompts.slider.folder_and_document_data_prompt import \
    build_slider_folder_and_document_data_prompt
from apps.core.slider.prompts.slider.whole_text_supplier_prompt import build_whole_text_supply_prompt_public, \
    build_whole_text_supply_prompt
from apps.core.slider.slider_executor import SliderExecutionManager
from apps.core.slider.slider_executor_public import SliderExecutionManager_Public

logger = logging.getLogger(__name__)


def build_auto_command_system_prompt(xc: SliderExecutionManager):
    logger.info(f"Building AUTO command system prompt.")

    combined_system_prompt = ""

    generic_instruction_prompt = ""
    generic_instruction_prompt += build_slider_agent_nickname_prompt(xc.copilot.name)
    generic_instruction_prompt += build_slider_internal_principles_prompt()
    generic_instruction_prompt += build_slider_agent_personality_prompt(tone=xc.copilot.tone)
    generic_instruction_prompt += build_slider_target_audience_prompt(audience=xc.copilot.audience)
    generic_instruction_prompt += build_slider_user_tenant_prompt(user=xc.copilot.created_by_user)
    generic_instruction_prompt += build_slider_spatial_awareness_prompt(user=xc.copilot.created_by_user)
    generic_instruction_prompt += build_slider_technical_dictionary_prompt(glossary=xc.copilot.glossary)

    folder_and_doc_info_prompt = build_slider_folder_and_document_data_prompt(
        folder=xc.slider_document.document_folder, doc=xc.slider_document)
    folder_and_doc_info_prompt += build_whole_text_supply_prompt(xc=xc)

    slider_ops_instruction_prompt = build_slider_ops_instruction_prompt()
    action_instructions_prompt = build_slider_action__auto_prompt(xc=xc)

    combined_system_prompt += generic_instruction_prompt
    combined_system_prompt += folder_and_doc_info_prompt
    combined_system_prompt += slider_ops_instruction_prompt
    combined_system_prompt += action_instructions_prompt

    return combined_system_prompt


def build_auto_command_system_prompt_public(xc: SliderExecutionManager_Public, content: str):
    logger.info(f"Building AUTO command system prompt.")

    combined_system_prompt = ""

    generic_instruction_prompt = ""
    generic_instruction_prompt += build_slider_agent_nickname_prompt(xc.copilot.name)
    generic_instruction_prompt += build_slider_internal_principles_prompt()
    generic_instruction_prompt += build_slider_agent_personality_prompt(tone=xc.copilot.tone)
    generic_instruction_prompt += build_slider_target_audience_prompt(audience=xc.copilot.audience)
    generic_instruction_prompt += build_slider_user_tenant_prompt(user=xc.copilot.created_by_user)
    generic_instruction_prompt += build_slider_spatial_awareness_prompt(user=xc.copilot.created_by_user)
    generic_instruction_prompt += build_slider_technical_dictionary_prompt(glossary=xc.copilot.glossary)

    folder_and_doc_info_prompt = build_whole_text_supply_prompt_public(content=content)

    slider_ops_instruction_prompt = build_slider_ops_instruction_prompt()
    action_instructions_prompt = build_slider_action__auto_prompt_public(content=content)

    combined_system_prompt += generic_instruction_prompt
    combined_system_prompt += folder_and_doc_info_prompt
    combined_system_prompt += slider_ops_instruction_prompt
    combined_system_prompt += action_instructions_prompt

    return combined_system_prompt
