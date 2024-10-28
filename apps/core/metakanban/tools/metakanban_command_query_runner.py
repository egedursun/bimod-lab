#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: metakanban_command_query_runner.py
#  Last Modified: 2024-10-27 20:12:32
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-27 20:12:32
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

from django.db import transaction, models

from apps.core.metakanban.utils import MetaKanbanCommandTypes
from apps.metakanban.models import MetaKanbanTaskLabel, MetaKanbanStatusColumn, MetaKanbanTask, MetaKanbanChangeLog, \
    MetaKanbanBoard
from apps.metakanban.utils import MetaKanbanChangeLogActionTypes, MetaKanbanTaskPrioritiesNames

logger = logging.getLogger(__name__)


def _metakanban_create_label_query(board_id: int, action_content: dict):
    board = MetaKanbanBoard.objects.get(id=board_id)
    label_name = action_content.get("label_name")
    label_color = action_content.get("label_color")

    created_object_id = None
    try:
        created_object = MetaKanbanTaskLabel.objects.create(
            board_id=board_id,
            label_name=label_name,
            label_color=label_color
        )
        created_object_id = created_object.id
    except Exception as e:
        logger.error(f"Error while creating label: {e}")
        return False, e

    try:
        # Add the change log for the change in the board.
        MetaKanbanChangeLog.objects.create(
            board=board,
            action_type=MetaKanbanChangeLogActionTypes.Label.CREATE_LABEL,
            action_details="Label '" + label_name + "' with the color '" + label_color + "' has been created.",
            change_by_user=None
        )
    except Exception as e:
        logger.error(f"Error while creating change log for label creation: {e}")

    return {
        "label_id": created_object_id,
    }, None


def _metakanban_update_label_query(board_id: int, action_content: dict):
    board = MetaKanbanBoard.objects.get(id=board_id)
    label_name = action_content.get("label_name")
    label_color = action_content.get("label_color")
    try:
        label = MetaKanbanTaskLabel.objects.get(id=action_content.get("label_id"))
        label.label_name = label_name
        label.label_color = label_color
        label.save()
    except Exception as e:
        logger.error(f"Error while updating label: {e}")
        return False, e

    try:
        # Add the change log for the change in the board.
        MetaKanbanChangeLog.objects.create(
            board=board,
            action_type=MetaKanbanChangeLogActionTypes.Label.UPDATE_LABEL,
            action_details="Label '" + label.label_name + "' has been updated to '" + label.label_name + "' and color has been updated to '" + label.label_color + "'.",
            change_by_user=None
        )
    except Exception as e:
        logger.error(f"Error while creating change log for label update: {e}")

    return True, None


def _metakanban_delete_label_query(board_id: int, action_content: dict):
    board = MetaKanbanBoard.objects.get(id=board_id)
    label_id = action_content.get("label_id")
    label = MetaKanbanTaskLabel.objects.get(id=label_id)
    label_name = label.label_name
    try:
        label.delete()
    except Exception as e:
        logger.error(f"Error while deleting label: {e}")
        return False, e

    try:
        # Add the change log for the change in the board.
        MetaKanbanChangeLog.objects.create(
            board=board,
            action_type=MetaKanbanChangeLogActionTypes.Label.DELETE_LABEL,
            action_details="Label '" + label_name + "' has been deleted.",
            change_by_user=None
        )
    except Exception as e:
        logger.error(f"Error while creating change log for label deletion: {e}")

    return True, None


def _metakanban_create_column_query(board_id: int, action_content: dict):
    board = MetaKanbanBoard.objects.get(id=board_id)
    column_name = action_content.get("column_name")

    def reorder_columns(b_id):
        cols = MetaKanbanStatusColumn.objects.filter(board_id=b_id).order_by("position_id")
        for index, col in enumerate(cols):
            if col.position_id != index:
                col.position_id = index
                col.save()

    created_object_id = None
    try:
        position_id = int(action_content.get("position_id"))
        with transaction.atomic():
            MetaKanbanStatusColumn.objects.filter(
                board_id=board_id, position_id__gte=position_id
            ).update(position_id=models.F("position_id") + 1)
            created_object = MetaKanbanStatusColumn.objects.create(
                board_id=board_id,
                column_name=column_name,
                position_id=position_id,
            )
            created_object_id = created_object.id
        reorder_columns(board_id)
    except Exception as e:
        logger.error(f"Error while creating column: {e}")
        return False, e

    try:
        # Add the change log for the change in the board.
        MetaKanbanChangeLog.objects.create(
            board=board,
            action_type=MetaKanbanChangeLogActionTypes.Column.CREATE_COLUMN,
            action_details="A new column created for the board, with the name: " + column_name,
            change_by_user=None
        )
    except Exception as e:
        logger.error(f"Error while creating change log for column creation: {e}")

    return {
        "column_id": created_object_id,
    }, None


def _metakanban_update_column_query(board_id: int, action_content: dict):
    board = MetaKanbanBoard.objects.get(id=board_id).first()
    updatable_column_id = action_content.get("column_id")
    new_column_name = action_content.get("column_name")
    updatable_position_id = action_content.get("position_id")
    updatable_column = MetaKanbanStatusColumn.objects.get(id=updatable_column_id).first()
    old_column_name = updatable_column.column_name

    def reorder_columns(b_id):
        cols = MetaKanbanStatusColumn.objects.filter(board_id=b_id).order_by("position_id")
        for index, col in enumerate(cols):
            if col.position_id != index:
                col.position_id = index
                col.save()

    try:
        column = updatable_column
        column.column_name = new_column_name
        column.position_id = updatable_position_id
        column.save()
        reorder_columns(board_id)
    except Exception as e:
        logger.error(f"Error while updating column: {e}")
        return False, e

    try:
        # Add the change log for the change in the board.
        MetaKanbanChangeLog.objects.create(
            board=board,
            action_type=MetaKanbanChangeLogActionTypes.Column.UPDATE_COLUMN,
            action_details="Column name updated from '" + old_column_name + "' to '" + new_column_name + "'.",
            change_by_user=None
        )
    except Exception as e:
        logger.error(f"Error while creating change log for column update: {e}")

    return True, None


def _metakanban_delete_column_query(board_id: int, action_content: dict):
    board = MetaKanbanBoard.objects.get(id=board_id).first()
    column_id = action_content.get("column_id")
    column = MetaKanbanStatusColumn.objects.get(id=column_id).first()
    column_name = column.column_name

    def reorder_columns(b_id):
        cols = MetaKanbanStatusColumn.objects.filter(board_id=b_id).order_by("position_id")
        for index, col in enumerate(cols):
            if col.position_id != index:
                col.position_id = index
                col.save()

    try:
        column = MetaKanbanStatusColumn.objects.get(id=action_content.get("column_id"))
        with transaction.atomic():
            column.delete()
            reorder_columns(board_id)
    except Exception as e:
        logger.error(f"Error while deleting column: {e}")
        return False, e

    try:
        # Add the change log for the change in the board.
        MetaKanbanChangeLog.objects.create(
            board=board,
            action_type=MetaKanbanChangeLogActionTypes.Column.DELETE_COLUMN,
            action_details="Column '" + column_name + "' has been deleted.",
            change_by_user=None
        )
    except Exception as e:
        logger.error(f"Error while creating change log for column deletion: {e}")

    return True, None


def _metakanban_create_task_query(board_id: int, action_content: dict):
    board = MetaKanbanBoard.objects.get(id=board_id)
    status_column_id = action_content.get("status_column_id")
    title = action_content.get("title")
    description = action_content.get("description", "")
    priority = action_content.get("priority", MetaKanbanTaskPrioritiesNames.UNCATEGORIZED)
    due_date = action_content.get("due_date", None)
    task_url = action_content.get("task_url", "")
    label_ids = action_content.get("label_ids", [])
    assignee_ids = action_content.get("assignee_ids", [])

    try:
        created_object = MetaKanbanTask.objects.create(
            board=board,
            status_column_id=status_column_id,
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            task_url=task_url
        )
        created_object.labels.set(label_ids)
        created_object.assignees.set(assignee_ids)
        created_object.save()
        created_object_id = created_object.id
    except Exception as e:
        logger.error(f"Error while creating task: {e}")
        return False, e

    try:
        # Add the change log for the change in the board.
        MetaKanbanChangeLog.objects.create(
            board=board,
            action_type=MetaKanbanChangeLogActionTypes.Task.CREATE_TASK,
            action_details="Task with the title '" + title + "' has been created.",
            change_by_user=None
        )
    except Exception as e:
        logger.error(f"Error while creating change log for task creation: {e}")

    return {
        "task_id": created_object_id,
    }, None


def _metakanban_update_task_query(board_id: int, action_content: dict):
    board = MetaKanbanBoard.objects.get(id=board_id)
    try:
        task = MetaKanbanTask.objects.get(id=action_content.get("task_id"))
        task.status_column_id = action_content.get("status_column_id", task.status_column_id)
        task.title = action_content.get("title", task.title)
        task.description = action_content.get("description", task.description)
        task.priority = action_content.get("priority", task.priority)
        task.due_date = action_content.get("due_date", task.due_date)
        task.task_url = action_content.get("task_url", task.task_url)
        task.labels.set(action_content.get("label_ids", task.labels.all()))
        task.assignees.set(action_content.get("assignee_ids", task.assignees.all()))
        task.save()
    except Exception as e:
        logger.error(f"Error while updating task: {e}")
        return False, e

    try:
        # Add the change log for the change in the board.
        created_object = MetaKanbanChangeLog.objects.create(
            board=board,
            action_type=MetaKanbanChangeLogActionTypes.Task.UPDATE_TASK,
            action_details="Task '" + task.title + "' information has been updated.",
            change_by_user=None
        )
    except Exception as e:
        logger.error(f"Error while creating change log for task update: {e}")

    return True, None


def _metakanban_delete_task_query(board_id: int, action_content: dict):
    board = MetaKanbanBoard.objects.get(id=board_id)
    task_id = action_content.get("task_id")
    task = MetaKanbanTask.objects.get(id=task_id)
    task_title = task.title
    try:
        task.delete()
    except Exception as e:
        logger.error(f"Error while deleting task: {e}")
        return False, e

    try:
        # Add the change log for the change in the board.
        MetaKanbanChangeLog.objects.create(
            board=board,
            action_type=MetaKanbanChangeLogActionTypes.Task.DELETE_TASK,
            action_details="Task '" + task_title + "' has been deleted.",
            change_by_user=None
        )
    except Exception as e:
        logger.error(f"Error while creating change log for task deletion: {e}")

    return True, None


def _metakanban_assign_task_query(board_id: int, action_content: dict):
    board = MetaKanbanBoard.objects.get(id=board_id)
    try:
        task = MetaKanbanTask.objects.get(id=action_content.get("task_id"))
        task.assignees.set(action_content.get("assignee_ids"))
        task.assignees.save()
        task.save()
    except Exception as e:
        logger.error(f"Error while assigning task: {e}")
        return False, e

    try:
        # Add the change log for the change in the board.
        MetaKanbanChangeLog.objects.create(
            board=board,
            action_type=MetaKanbanChangeLogActionTypes.Task.ASSIGN_TASK,
            action_details="Users assigned to task '" + task.title + "' as follows: " + ", ".join(
                [assignee.username for assignee in task.assignees.all()]),
            change_by_user=None
        )
    except Exception as e:
        logger.error(f"Error while creating change log for task assignment: {e}")

    return True, None


def _metakanban_move_task_query(board_id: int, action_content: dict):
    board = MetaKanbanBoard.objects.get(id=board_id)
    try:
        task = MetaKanbanTask.objects.get(id=action_content.get("task_id"))
        task.status_column_id = action_content.get("status_column_id")
        task.save()
    except Exception as e:
        logger.error(f"Error while moving task: {e}")
        return False, e

    try:
        # Add the change log for the change in the board.
        MetaKanbanChangeLog.objects.create(
            board=board,
            action_type=MetaKanbanChangeLogActionTypes.Task.MOVE_TASK,
            action_details="Task '" + task.title + "' has encountered a status change and switched columns.",
            change_by_user=None
        )
    except Exception as e:
        logger.error(f"Error while creating change log for task move: {e}")

    return True, None


#####################################################################################################################


def run_metakanban_command_query(board_id: int, action_type: str, action_content: dict):
    if action_type == MetaKanbanCommandTypes.CREATE_LABEL:
        output, error = _metakanban_create_label_query(board_id, action_content)
    elif action_type == MetaKanbanCommandTypes.UPDATE_LABEL:
        output, error = _metakanban_update_label_query(board_id, action_content)
    elif action_type == MetaKanbanCommandTypes.DELETE_LABEL:
        output, error = _metakanban_delete_label_query(board_id, action_content)
    elif action_type == MetaKanbanCommandTypes.CREATE_COLUMN:
        output, error = _metakanban_create_column_query(board_id, action_content)
    elif action_type == MetaKanbanCommandTypes.UPDATE_COLUMN:
        output, error = _metakanban_update_column_query(board_id, action_content)
    elif action_type == MetaKanbanCommandTypes.DELETE_COLUMN:
        output, error = _metakanban_delete_column_query(board_id, action_content)
    elif action_type == MetaKanbanCommandTypes.CREATE_TASK:
        output, error = _metakanban_create_task_query(board_id, action_content)
    elif action_type == MetaKanbanCommandTypes.UPDATE_TASK:
        output, error = _metakanban_update_task_query(board_id, action_content)
    elif action_type == MetaKanbanCommandTypes.DELETE_TASK:
        output, error = _metakanban_delete_task_query(board_id, action_content)
    elif action_type == MetaKanbanCommandTypes.ASSIGN_TASK:
        output, error = _metakanban_assign_task_query(board_id, action_content)
    elif action_type == MetaKanbanCommandTypes.MOVE_TASK:
        output, error = _metakanban_move_task_query(board_id, action_content)
    else:
        return False, f"Invalid action type: {action_type}"
    return output, error
