#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: assign_board_task_views.py
#  Last Modified: 2024-10-27 00:07:04
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-27 00:07:04
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


class MetaKanbanView_TaskAssign(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        task_id = request.POST.get("task_id")
        task = get_object_or_404(MetaKanbanTask, id=task_id)
        board = task.board

        ##############################
        # PERMISSION CHECK FOR - ASSIGN_METAKANBAN_TASK
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ASSIGN_METAKANBAN_TASK):
            messages.error(self.request, "You do not have permission to assign users to a kanban task.")
            return redirect('metakanban:board_detail', board_id=task.board.id)
        ##############################

        assignee_ids = request.POST.getlist("assignees")
        task.assignees.set(assignee_ids)
        task.save()

        try:
            # Add the change log for the change in the board.
            MetaKanbanChangeLog.objects.create(
                board=board,
                action_type=MetaKanbanChangeLogActionTypes.Task.ASSIGN_TASK,
                action_details="Users assigned to task '" + task.title + "' as follows: " + ", ".join([assignee.username for assignee in task.assignees.all()]),
                change_by_user=request.user
            )
        except Exception as e:
            messages.error(request, "Task change log could not be created. Error: " + str(e))

        messages.success(request, f"Users assigned to task '{task.title}' successfully.")
        return redirect("metakanban:board_detail", board_id=task.board.id)
