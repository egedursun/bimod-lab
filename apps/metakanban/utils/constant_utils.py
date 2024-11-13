#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-10-23 17:34:38
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-23 17:34:39
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


META_KANBAN_TASK_PRIORITIES = [
    ('uncategorized', 'Uncategorized'),
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
    ('urgent', 'Urgent'),
]


class MetaKanbanTaskPrioritiesNames:
    UNCATEGORIZED = 'uncategorized'
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    URGENT = 'urgent'

    @staticmethod
    def as_list():
        return [MetaKanbanTaskPrioritiesNames.UNCATEGORIZED, MetaKanbanTaskPrioritiesNames.LOW,
                MetaKanbanTaskPrioritiesNames.MEDIUM, MetaKanbanTaskPrioritiesNames.HIGH,
                MetaKanbanTaskPrioritiesNames.URGENT]


META_KANBAN_BOARD_ADMIN_LIST = ['id', 'project', 'llm_model', 'title', 'created_by_user', 'created_at', 'updated_at']
META_KANBAN_BOARD_ADMIN_FILTER = ['id', 'project', 'llm_model', 'title', 'created_by_user', 'created_at', 'updated_at']
META_KANBAN_BOARD_ADMIN_SEARCH = ['id', 'project', 'llm_model', 'title', 'created_by_user', 'created_at', 'updated_at']

META_KANBAN_CHANGE_LOG_ACTION_TYPES = [
    # Tasks
    ('create_task', 'Create Task'),
    ('update_task', 'Update Task'),
    ('delete_task', 'Delete Task'),
    ('move_task', 'Move Task'),
    ('assign_task', 'Assign Task'),
    # Column
    ('create_column', 'Create Column'),
    ('update_column', 'Update Column'),
    ('delete_column', 'Delete Column'),
    ('move_column', 'Move Column'),
    # Label
    ('create_label', 'Create Label'),
    ('update_label', 'Update Label'),
    ('delete_label', 'Delete Label'),
]


class MetaKanbanChangeLogActionTypes:
    class Task:
        CREATE_TASK = 'create_task'
        UPDATE_TASK = 'update_task'
        DELETE_TASK = 'delete_task'
        MOVE_TASK = 'move_task'
        ASSIGN_TASK = 'assign_task'

        @staticmethod
        def as_list():
            return [MetaKanbanChangeLogActionTypes.Task.CREATE_TASK, MetaKanbanChangeLogActionTypes.Task.UPDATE_TASK,
                    MetaKanbanChangeLogActionTypes.Task.DELETE_TASK, MetaKanbanChangeLogActionTypes.Task.MOVE_TASK,
                    MetaKanbanChangeLogActionTypes.Task.ASSIGN_TASK]

    class Column:
        CREATE_COLUMN = 'create_column'
        UPDATE_COLUMN = 'update_column'
        DELETE_COLUMN = 'delete_column'
        MOVE_COLUMN = 'move_column'

        @staticmethod
        def as_list():
            return [MetaKanbanChangeLogActionTypes.Column.CREATE_COLUMN,
                    MetaKanbanChangeLogActionTypes.Column.UPDATE_COLUMN,
                    MetaKanbanChangeLogActionTypes.Column.DELETE_COLUMN,
                    MetaKanbanChangeLogActionTypes.Column.MOVE_COLUMN]

    class Label:
        CREATE_LABEL = 'create_label'
        UPDATE_LABEL = 'update_label'
        DELETE_LABEL = 'delete_label'

        @staticmethod
        def as_list():
            return [MetaKanbanChangeLogActionTypes.Label.CREATE_LABEL,
                    MetaKanbanChangeLogActionTypes.Label.UPDATE_LABEL,
                    MetaKanbanChangeLogActionTypes.Label.DELETE_LABEL]

    @staticmethod
    def as_list():
        return [
            MetaKanbanChangeLogActionTypes.Task.CREATE_TASK, MetaKanbanChangeLogActionTypes.Task.UPDATE_TASK,
            MetaKanbanChangeLogActionTypes.Task.DELETE_TASK, MetaKanbanChangeLogActionTypes.Task.MOVE_TASK,
            MetaKanbanChangeLogActionTypes.Task.ASSIGN_TASK, MetaKanbanChangeLogActionTypes.Column.CREATE_COLUMN,
            MetaKanbanChangeLogActionTypes.Column.UPDATE_COLUMN, MetaKanbanChangeLogActionTypes.Column.DELETE_COLUMN,
            MetaKanbanChangeLogActionTypes.Column.MOVE_COLUMN, MetaKanbanChangeLogActionTypes.Label.CREATE_LABEL,
            MetaKanbanChangeLogActionTypes.Label.UPDATE_LABEL, MetaKanbanChangeLogActionTypes.Label.DELETE_LABEL,
        ]


META_KANBAN_CHANGE_LOG_ADMIN_LIST = ['board', 'action_type', 'change_by_user', 'timestamp']
META_KANBAN_CHANGE_LOG_ADMIN_FILTER = ['board', 'action_type', 'change_by_user']
META_KANBAN_CHANGE_LOG_ADMIN_SEARCH = ['board', 'action_type', 'change_by_user']

META_KANBAN_STATUS_COLUMN_LIST = ('id', 'board', 'column_name', 'position_id', 'created_by_user',
                                  'created_at', 'updated_at')
META_KANBAN_STATUS_COLUMN_FILTER = ('board', 'created_by_user', 'created_at', 'updated_at')
META_KANBAN_STATUS_COLUMN_SEARCH = ('column_name',)

META_KANBAN_TASK_ADMIN_LIST = ['title', 'board', 'status_column', 'priority', 'due_date',
                               'created_by_user', 'created_at', 'updated_at']
META_KANBAN_TASK_ADMIN_FILTER = ['board', 'status_column', 'priority', 'due_date', 'created_by_user',
                                 'created_at', 'updated_at']
META_KANBAN_TASK_ADMIN_SEARCH = ('title',)

META_KANBAN_TASK_LABEL_COLOR_CHOICES = [
    ('#FF0000', 'Red'),
    ('#FFA500', 'Orange'),
    ('#FFFF00', 'Yellow'),
    ('#008000', 'Green'),
    ('#008080', 'Teal'),
    ('#0000FF', 'Blue'),
    ('#000080', 'Navy'),
    ('#EE82EE', 'Violet'),
    ('#FFC0CB', 'Pink'),
    ('#000000', 'Black'),
    ('#A52A2A', 'Brown'),
    ('#FFFFFF', 'White'),
    ('#808080', 'Gray'),
]


class MetaKanbanTaskLabelColorChoiceNames:
    RED = '#FF0000'
    ORANGE = '#FFA500'
    YELLOW = '#FFFF00'
    GREEN = '#008000'
    TEAL = '#008080'
    BLUE = '#0000FF'
    NAVY = '#000080'
    VIOLET = '#EE82EE'
    PINK = '#FFC0CB'
    BLACK = '#000000'
    BROWN = '#A52A2A'
    WHITE = '#FFFFFF'
    GRAY = '#808080'

    @staticmethod
    def as_list():
        return [
            MetaKanbanTaskLabelColorChoiceNames.RED,
            MetaKanbanTaskLabelColorChoiceNames.ORANGE,
            MetaKanbanTaskLabelColorChoiceNames.YELLOW,
            MetaKanbanTaskLabelColorChoiceNames.GREEN,
            MetaKanbanTaskLabelColorChoiceNames.TEAL,
            MetaKanbanTaskLabelColorChoiceNames.BLUE,
            MetaKanbanTaskLabelColorChoiceNames.NAVY,
            MetaKanbanTaskLabelColorChoiceNames.VIOLET,
            MetaKanbanTaskLabelColorChoiceNames.PINK,
            MetaKanbanTaskLabelColorChoiceNames.BLACK,
            MetaKanbanTaskLabelColorChoiceNames.BROWN,
            MetaKanbanTaskLabelColorChoiceNames.WHITE,
            MetaKanbanTaskLabelColorChoiceNames.GRAY,
        ]


META_KANBAN_TASK_LABEL_ADMIN_LIST = ('label_name', 'label_color', 'created_by_user', 'created_at', 'updated_at')
META_KANBAN_TASK_LABEL_ADMIN_FILTER = ('label_color', 'created_by_user', 'created_at', 'updated_at')
META_KANBAN_TASK_LABEL_ADMIN_SEARCH = ('label_name',)

META_KANBAN_MEETING_TRANSCRIPTION_ADMIN_LIST = ('board', 'is_processed_with_ai', 'created_at', 'updated_at')
META_KANBAN_MEETING_TRANSCRIPTION_ADMIN_FILTER = ('is_processed_with_ai', 'created_at', 'updated_at')
META_KANBAN_MEETING_TRANSCRIPTION_ADMIN_SEARCH = ('board', 'meeting_transcription_text',
                                                  'meeting_transcription_key_takeaways')


META_KANBAN_BOARD_API_KEY_DEFAULT_LENGTH = 64
METAKANBAN_ASSISTANT_CONNECTION_ADMIN_LIST = ["metakanban_board", "assistant", "created_by_user", "created_at", "updated_at"]
METAKANBAN_ASSISTANT_CONNECTION_ADMIN_SEARCH = ["metakanban_board__name", "assistant__name", "created_by_user__username"]
METAKANBAN_ASSISTANT_CONNECTION_ADMIN_FILTER = ["created_at", "updated_at"]
