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
    # Columns
    ('create_column', 'Create Column'),
    ('update_column', 'Update Column'),
    ('delete_column', 'Delete Column'),
    # Comments
    ('create_comment', 'Create Comment'),
    ('update_comment', 'Update Comment'),
    ('delete_comment', 'Delete Comment'),
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
        COLUMN_REORDER = 'column_reorder'

        @staticmethod
        def as_list():
            return [MetaKanbanChangeLogActionTypes.Column.CREATE_COLUMN,
                    MetaKanbanChangeLogActionTypes.Column.UPDATE_COLUMN,
                    MetaKanbanChangeLogActionTypes.Column.DELETE_COLUMN,
                    MetaKanbanChangeLogActionTypes.Column.COLUMN_REORDER]

    class Comment:
        CREATE_COMMENT = 'create_comment'
        UPDATE_COMMENT = 'update_comment'
        DELETE_COMMENT = 'delete_comment'

        @staticmethod
        def as_list():
            return [MetaKanbanChangeLogActionTypes.Comment.CREATE_COMMENT,
                    MetaKanbanChangeLogActionTypes.Comment.UPDATE_COMMENT,
                    MetaKanbanChangeLogActionTypes.Comment.DELETE_COMMENT]

    @staticmethod
    def as_list():
        return [MetaKanbanChangeLogActionTypes.Task.CREATE_TASK,
                MetaKanbanChangeLogActionTypes.Task.UPDATE_TASK,
                MetaKanbanChangeLogActionTypes.Task.DELETE_TASK,
                MetaKanbanChangeLogActionTypes.Task.MOVE_TASK,
                MetaKanbanChangeLogActionTypes.Task.ASSIGN_TASK,

                MetaKanbanChangeLogActionTypes.Column.CREATE_COLUMN,
                MetaKanbanChangeLogActionTypes.Column.UPDATE_COLUMN,
                MetaKanbanChangeLogActionTypes.Column.DELETE_COLUMN,
                MetaKanbanChangeLogActionTypes.Column.COLUMN_REORDER,

                MetaKanbanChangeLogActionTypes.Comment.CREATE_COMMENT,
                MetaKanbanChangeLogActionTypes.Comment.UPDATE_COMMENT,
                MetaKanbanChangeLogActionTypes.Comment.DELETE_COMMENT]


META_KANBAN_CHANGE_LOG_ADMIN_LIST = ['board', 'action_type', 'change_by_user', 'timestamp']
META_KANBAN_CHANGE_LOG_ADMIN_FILTER = ['board', 'action_type', 'change_by_user']
META_KANBAN_CHANGE_LOG_ADMIN_SEARCH = ['board', 'action_type', 'change_by_user']

META_KANBAN_STATUS_COLUMN_LIST = ('id', 'board', 'column_name', 'position_id', 'created_by_user',
                                  'created_at', 'updated_at')
META_KANBAN_STATUS_COLUMN_FILTER = ('board', 'created_by_user', 'created_at', 'updated_at')
META_KANBAN_STATUS_COLUMN_SEARCH = ('column_name',)

META_KANBAN_COMMENT_ADMIN_LIST = ['task', 'comment_by_user', 'created_at', 'updated_at']
META_KANBAN_COMMENT_ADMIN_SEARCH = ['task', 'comment_by_user']
META_KANBAN_COMMENT_ADMIN_FILTER = ['created_at', 'updated_at', 'task', 'comment_by_user']

META_KANBAN_TASK_ADMIN_LIST = ['title', 'board', 'status_column', 'priority', 'due_date', 'assignee',
                               'created_by_user', 'created_at', 'updated_at']
META_KANBAN_TASK_ADMIN_FILTER = ['board', 'status_column', 'priority', 'due_date', 'assignee', 'created_by_user',
                                 'created_at', 'updated_at']
META_KANBAN_TASK_ADMIN_SEARCH = ('title',)
