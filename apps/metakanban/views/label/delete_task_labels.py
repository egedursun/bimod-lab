#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_task_labels.py
#  Last Modified: 2024-10-27 00:34:03
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-27 00:34:04
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


class MetaKanbanView_LabelDelete(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        board_id = kwargs.get("board_id")
        board = get_object_or_404(MetaKanbanBoard, id=board_id)

        ##############################
        # PERMISSION CHECK FOR - DELETE_METAKANBAN_TASK_LABEL
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_METAKANBAN_TASK_LABEL):
            messages.error(self.request, "You do not have permission to delete a kanban task label.")
            return redirect('metakanban:board_detail', board_id=board_id)
        ##############################

        try:
            label_id = kwargs.get("label_id")
            label = get_object_or_404(MetaKanbanTaskLabel, id=label_id)
            label_name = label.label_name
            label.delete()
        except Exception as e:
            messages.error(request, "Label could not be deleted. Error: " + str(e))
            return redirect("metakanban:label_list", board_id=board_id)

        try:
            # Add the change log for the change in the board.
            MetaKanbanChangeLog.objects.create(
                board=board,
                action_type=MetaKanbanChangeLogActionTypes.Label.DELETE_LABEL,
                action_details="Label '" + label_name + "' has been deleted.",
                change_by_user=request.user
            )
        except Exception as e:
            messages.error(request, "Label change log could not be created. Error: " + str(e))

        messages.success(request, f'Label "{label_name}" deleted successfully.')
        return redirect("metakanban:label_list", board_id=board_id)
