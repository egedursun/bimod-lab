#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: update_task_label.py
#  Last Modified: 2024-10-27 00:33:49
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-27 00:33:49
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
from apps.metakanban.models import MetaKanbanTaskLabel, MetaKanbanChangeLog, MetaKanbanBoard
from apps.metakanban.utils import MetaKanbanChangeLogActionTypes
from apps.user_permissions.utils import PermissionNames


class MetaKanbanView_LabelUpdate(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        board_id = kwargs.get("board_id")
        board = get_object_or_404(MetaKanbanBoard, id=board_id)

        ##############################
        # PERMISSION CHECK FOR - UPDATE_METAKANBAN_TASK_LABEL
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_METAKANBAN_TASK_LABEL):
            messages.error(self.request, "You do not have permission to update a kanban task label.")
            return redirect('metakanban:board_detail', board_id=board_id)
        ##############################

        label_id = kwargs.get("label_id")
        label = get_object_or_404(MetaKanbanTaskLabel, id=label_id, board_id=board_id)

        label.label_name = request.POST.get("label_name", label.label_name)
        label.label_color = request.POST.get("label_color", label.label_color)
        label.save()

        try:
            # Add the change log for the change in the board.
            MetaKanbanChangeLog.objects.create(
                board=board,
                action_type=MetaKanbanChangeLogActionTypes.Label.UPDATE_LABEL,
                action_details="Label '" + label.label_name + "' has been updated to '" + label.label_name + "' and color has been updated to '" + label.label_color + "'.",
                change_by_user=request.user
            )
        except Exception as e:
            messages.error(request, "Label change log could not be created. Error: " + str(e))

        messages.success(request, "Label updated successfully.")
        return redirect("metakanban:label_list", board_id=board_id)
