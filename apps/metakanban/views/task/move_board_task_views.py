#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: move_task.py
#  Last Modified: 2024-10-26 23:50:27
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-26 23:50:28
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.metakanban.models import MetaKanbanTask, MetaKanbanChangeLog
from apps.metakanban.utils import MetaKanbanChangeLogActionTypes
from apps.user_permissions.utils import PermissionNames


class MetaKanbanView_TaskMove(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        task_id = request.POST.get("task_id")
        task = get_object_or_404(MetaKanbanTask, id=task_id)
        board = task.board

        ##############################
        # PERMISSION CHECK FOR - MOVE_METAKANBAN_TASK
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.MOVE_METAKANBAN_TASK):
            messages.error(self.request, "You do not have permission to move a kanban task.")
            return redirect('metakanban:board_detail', board_id=task.board.id)
        ##############################

        new_status_column_id = request.POST.get("column_id")
        if new_status_column_id:
            task.status_column_id = new_status_column_id
            task.save()
            messages.success(request, f'Task "{task.title}" moved to the new column successfully.')
        else:
            messages.error(request, "Invalid status column.")

        try:
            # Add the change log for the change in the board.
            MetaKanbanChangeLog.objects.create(
                board=board,
                action_type=MetaKanbanChangeLogActionTypes.Task.MOVE_TASK,
                action_details="Task '" + task.title + "' has encountered a status change and switched columns.",
                change_by_user=request.user
            )
        except Exception as e:
            messages.error(request, "Task change log could not be created. Error: " + str(e))

        return redirect("metakanban:board_detail", board_id=task.board.id)
