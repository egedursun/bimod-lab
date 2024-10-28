#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-10-23 17:37:43
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-23 17:37:43
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
from apps.metakanban.utils import MetaKanbanTaskLabelColorChoiceNames, MetaKanbanTaskPrioritiesNames

METAKANBAN_TOOL_COMMAND_MAXIMUM_ATTEMPTS = 10

METAKANBAN_DEFAULT_LAST_N_ACTION_LOGS_LOOKBACK = 50


class MetaKanbanCommandTypes:
    CREATE_LABEL = "CREATE_LABEL"
    UPDATE_LABEL = "UPDATE_LABEL"
    DELETE_LABEL = "DELETE_LABEL"

    CREATE_COLUMN = "CREATE_COLUMN"
    UPDATE_COLUMN = "UPDATE_COLUMN"
    DELETE_COLUMN = "DELETE_COLUMN"

    CREATE_TASK = "CREATE_TASK"
    UPDATE_TASK = "UPDATE_TASK"
    DELETE_TASK = "DELETE_TASK"
    ASSIGN_TASK = "ASSIGN_TASK"
    MOVE_TASK = "MOVE_TASK"

    @staticmethod
    def as_list():
        return [
            MetaKanbanCommandTypes.CREATE_LABEL,
            MetaKanbanCommandTypes.UPDATE_LABEL,
            MetaKanbanCommandTypes.DELETE_LABEL,
            MetaKanbanCommandTypes.CREATE_COLUMN,
            MetaKanbanCommandTypes.UPDATE_COLUMN,
            MetaKanbanCommandTypes.DELETE_COLUMN,
            MetaKanbanCommandTypes.CREATE_TASK,
            MetaKanbanCommandTypes.UPDATE_TASK,
            MetaKanbanCommandTypes.DELETE_TASK,
            MetaKanbanCommandTypes.ASSIGN_TASK,
            MetaKanbanCommandTypes.MOVE_TASK
        ]

    @staticmethod
    def as_tool_dict_guide():
        return {
            MetaKanbanCommandTypes.CREATE_LABEL: {
                "label_name": "<string value here>",
                "label_color": f"""<One of these values here: {MetaKanbanTaskLabelColorChoiceNames.as_list()}>""",
            },
            MetaKanbanCommandTypes.UPDATE_LABEL: {
                "label_id": "<integer value here>",
                "label_name": "<string value here>",
                "label_color": "<string value here>",
            },
            MetaKanbanCommandTypes.DELETE_LABEL: {
                "label_id": "<integer value here>",
            },
            MetaKanbanCommandTypes.CREATE_COLUMN: {
                "column_name": "<string value here>",
                "position_id": "<integer value here>",
            },
            MetaKanbanCommandTypes.UPDATE_COLUMN: {
                "column_id": "<integer value here>",
                "column_name": "<string value here>",
                "position_id": "<integer value here>",
            },
            MetaKanbanCommandTypes.DELETE_COLUMN: {
                "column_id": "<integer value here>",
            },
            MetaKanbanCommandTypes.CREATE_TASK: {
                "status_column_id": "<integer value here>",
                "title": "<string value here>",
                "description": "<string value here>",
                "label_ids": ["<integer value here>", "<integer value here>", "..."],
                "priority": f"""<One of these values here: {MetaKanbanTaskPrioritiesNames.as_list()}>""",
                "due_date": "<datetime value here>",
                "assignee_ids": ["<integer value here>", "<integer value here>", "..."],
                "task_url": "<string value here>"
            },
            MetaKanbanCommandTypes.UPDATE_TASK: {
                "task_id": "<integer value here>",
                "status_column_id": "<integer value here>",
                "title": "<string value here>",
                "description": "<string value here>",
                "label_ids": ["<integer value here>", "<integer value here>", "..."],
                "priority": f"""<One of these values here: {MetaKanbanTaskPrioritiesNames.as_list()}>""",
                "due_date": "<datetime value here>",
                "assignee_ids": ["<integer value here>", "<integer value here>", "..."],
                "task_url": "<string value here>"
            },
            MetaKanbanCommandTypes.DELETE_TASK: {
                "task_id": "<integer value here>",
            },
            MetaKanbanCommandTypes.ASSIGN_TASK: {
                "task_id": "<integer value here>",
                "assignee_ids": ["<integer value here>", "<integer value here>", "..."],
            },
            MetaKanbanCommandTypes.MOVE_TASK: {
                "task_id": "<integer value here>",
                "status_column_id": "<integer value here>",
            },
        }
