#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: metakanban_prompt_builder.py
#  Last Modified: 2024-10-27 19:53:56
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-27 19:53:57
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from apps.core.metakanban.prompts import (get_generic_instructions_metakanban,
                                          get_metakanban_project_metadata_prompt, get_board_metadata_prompt,
                                          get_metakanban_last_n_action_logs_prompt,
                                          get_board_existing_tasks_metadata_prompt, get_board_labels_metadata_prompt,
                                          get_tool_prompt_metakanban_command_execution,
                                          get_latest_meeting_transcriptions_prompt)
from apps.core.system_prompts.tool_call_prompts.generic_instructions_tool_call import \
    build_lean_structured_tool_usage_instructions_prompt
from apps.metakanban.models import MetaKanbanBoard


def build_metakanban_agent_prompts(board: MetaKanbanBoard):
    merged_prompt = ""

    merged_prompt += get_generic_instructions_metakanban(board=board)
    merged_prompt += get_board_metadata_prompt(board=board)
    merged_prompt += get_board_labels_metadata_prompt(board=board)
    merged_prompt += get_board_existing_tasks_metadata_prompt(board=board)
    merged_prompt += get_metakanban_last_n_action_logs_prompt(board=board)
    merged_prompt += get_metakanban_project_metadata_prompt(board=board)
    merged_prompt += get_latest_meeting_transcriptions_prompt(board=board)
    merged_prompt += build_lean_structured_tool_usage_instructions_prompt()
    merged_prompt += get_tool_prompt_metakanban_command_execution()

    return merged_prompt
