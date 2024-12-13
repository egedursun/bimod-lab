#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_board_task.py
#  Last Modified: 2024-10-26 23:46:24
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-26 23:46:25
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
    MetaKanbanBoard,
    MetaKanbanTask,
    MetaKanbanChangeLog
)

from apps.metakanban.utils import (
    MetaKanbanChangeLogActionTypes
)

from apps.user_permissions.utils import (
    PermissionNames
)


class MetaKanbanView_TaskCreate(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        board_id = request.POST.get("board_id")

        board = get_object_or_404(
            MetaKanbanBoard,
            id=board_id
        )

        ##############################
        # PERMISSION CHECK FOR - ADD_METAKANBAN_TASK
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.ADD_METAKANBAN_TASK
        ):
            messages.error(self.request, "You do not have permission to add a kanban task.")

            return redirect(
                'metakanban:board_detail',
                board_id=board_id
            )
        ##############################

        title = request.POST.get("title")
        status_column_id = request.POST.get("column_id")

        if title and status_column_id:
            task = MetaKanbanTask.objects.create(
                board=board,
                title=title,
                status_column_id=status_column_id,
                created_by_user=request.user,
            )
            messages.success(request, f'Task "{task.title}" created successfully.')

        else:
            messages.error(request, "Title and Status Column are required to create a task.")

        try:
            MetaKanbanChangeLog.objects.create(
                board=board,
                action_type=MetaKanbanChangeLogActionTypes.Task.CREATE_TASK,
                action_details="Task with the title '" + title + "' has been created.",
                change_by_user=request.user
            )

        except Exception as e:
            messages.error(request, "Task change log could not be created. Error: " + str(e))

        return redirect(
            "metakanban:board_detail",
            board_id=board.id
        )
