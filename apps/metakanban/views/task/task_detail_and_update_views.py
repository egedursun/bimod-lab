#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: task_detail_and_update_views.py
#  Last Modified: 2024-10-26 23:56:20
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-26 23:56:20
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

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.shortcuts import (
    get_object_or_404,
    redirect
)

from django.utils.dateparse import (
    parse_datetime
)

from django.views import View

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.metakanban.models import (
    MetaKanbanTask,
    MetaKanbanTaskLabel,
    MetaKanbanChangeLog
)

from apps.metakanban.utils import (
    MetaKanbanChangeLogActionTypes
)

from apps.user_permissions.utils import (
    PermissionNames
)


class MetaKanbanView_TaskDetailAndUpdate(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        task_id = request.POST.get("task_id")

        task = get_object_or_404(
            MetaKanbanTask,
            id=task_id
        )

        board = task.board

        ##############################
        # PERMISSION CHECK FOR - UPDATE_METAKANBAN_TASK
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.UPDATE_METAKANBAN_TASK
        ):
            messages.error(self.request, "You do not have permission to update a kanban task.")

            return redirect(
                'metakanban:board_detail',
                board_id=task.board.id
            )
        ##############################

        task.description = request.POST.get("description", task.description)
        label_ids = request.POST.getlist("labels")

        task.labels.set(
            MetaKanbanTaskLabel.objects.filter(
                id__in=label_ids
            )
        )

        assigned_user_ids = request.POST.getlist("assignees")
        task.assignees.set(assigned_user_ids)

        task.priority = request.POST.get(
            "priority",
            task.priority
        )

        task.due_date = parse_datetime(
            request.POST.get("due_date")
        ) if request.POST.get("due_date") else task.due_date

        task.task_url = request.POST.get(
            "task_url",
            task.task_url
        )

        if "task_file" in request.FILES:
            task.task_file = request.FILES["task_file"]

        if "task_image" in request.FILES:
            task.task_image = request.FILES["task_image"]

        task.save()

        try:
            MetaKanbanChangeLog.objects.create(
                board=board,
                action_type=MetaKanbanChangeLogActionTypes.Task.UPDATE_TASK,
                action_details="Task '" + task.title + "' information has been updated.",
                change_by_user=request.user
            )

        except Exception as e:
            messages.error(request, "Task change log could not be created. Error: " + str(e))

        messages.success(request, f'Task "{task.title}" updated successfully.')

        return redirect(
            "metakanban:board_detail",
            board_id=task.board.id
        )
