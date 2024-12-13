#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_board_task.py
#  Last Modified: 2024-10-26 23:46:31
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-26 23:46:31
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

from django.views import View

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.metakanban.models import (
    MetaKanbanTask,
    MetaKanbanChangeLog
)

from apps.metakanban.utils import (
    MetaKanbanChangeLogActionTypes
)

from apps.user_permissions.utils import (
    PermissionNames
)


class MetaKanbanView_TaskDelete(LoginRequiredMixin, View):

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
        # PERMISSION CHECK FOR - DELETE_METAKANBAN_TASK
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_METAKANBAN_TASK
        ):
            messages.error(self.request, "You do not have permission to delete a kanban task.")

            return redirect(
                'metakanban:board_detail',
                board_id=task.board.id
            )
        ##############################

        task_title = task.title

        task.delete()

        try:
            MetaKanbanChangeLog.objects.create(
                board=board,
                action_type=MetaKanbanChangeLogActionTypes.Task.DELETE_TASK,
                action_details="Task '" + task_title + "' has been deleted.",
                change_by_user=request.user
            )

        except Exception as e:
            messages.error(request, "Task change log could not be created. Error: " + str(e))

        messages.success(request, f'Task "{task_title}" deleted successfully.')

        return redirect(
            "metakanban:board_detail",
            board_id=task.board.id
        )
