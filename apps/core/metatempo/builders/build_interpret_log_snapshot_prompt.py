#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: build_interpret_log_snapshot_prompt.py
#  Last Modified: 2024-10-29 16:03:25
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-29 16:03:26
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from apps.core.metatempo.prompts import (
    get_generic_member_log_snapshot_prompt,
    get_board_metadata_prompt,
    get_board_labels_metadata_prompt,
    get_board_existing_tasks_metadata_prompt,
    get_metakanban_last_n_action_logs_prompt,
    get_metakanban_project_metadata_prompt,
    get_connection_metadata_prompt
)

from apps.metatempo.models import MetaTempoConnection


def build_log_snapshot_interpretation_prompt(
    connection: MetaTempoConnection
):
    board = connection.board

    merged_prompt = f""
    merged_prompt += get_generic_member_log_snapshot_prompt()
    merged_prompt += get_connection_metadata_prompt(
        connection=connection
    )
    merged_prompt += get_board_metadata_prompt(
        board=board
    )
    merged_prompt += get_board_labels_metadata_prompt(
        board=board
    )
    merged_prompt += get_board_existing_tasks_metadata_prompt(
        board=board
    )
    merged_prompt += get_metakanban_last_n_action_logs_prompt(
        board=board
    )
    merged_prompt += get_metakanban_project_metadata_prompt(
        board=board
    )
    return merged_prompt
