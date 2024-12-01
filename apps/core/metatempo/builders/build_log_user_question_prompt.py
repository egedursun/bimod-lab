#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: build_log_user_question_prompt.py
#  Last Modified: 2024-10-29 16:52:02
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-29 16:52:03
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
    get_generic_ask_question_prompt,
    get_overall_logs_datasource_prompt,
    get_board_metadata_prompt,
    get_board_labels_metadata_prompt,
    get_board_existing_tasks_metadata_prompt,
    get_metakanban_last_n_action_logs_prompt,
    get_metakanban_project_metadata_prompt,
    get_connection_metadata_prompt
)

from apps.metatempo.models import MetaTempoConnection


def build_user_loq_question_interpretation_prompt(
    connection: MetaTempoConnection,
    batched_logs: list
):
    board = connection.board

    merged_prompt = f""
    merged_prompt += get_generic_ask_question_prompt()
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
    merged_prompt += get_overall_logs_datasource_prompt(
        connection=connection,
        batched_logs=batched_logs
    )
    return merged_prompt
