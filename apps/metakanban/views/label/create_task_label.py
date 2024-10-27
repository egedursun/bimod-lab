#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_task_label.py
#  Last Modified: 2024-10-27 00:33:41
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-27 00:33:42
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
from apps.metakanban.models import MetaKanbanBoard, MetaKanbanTaskLabel
from apps.user_permissions.utils import PermissionNames


class MetaKanbanView_LabelCreate(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        board_id = kwargs.get("board_id")

        ##############################
        # PERMISSION CHECK FOR - ADD_METAKANBAN_TASK_LABEL
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_METAKANBAN_TASK_LABEL):
            messages.error(self.request, "You do not have permission to add a kanban task label.")
            return redirect('metakanban:board_detail', board_id=board_id)
        ##############################

        board = get_object_or_404(MetaKanbanBoard, id=board_id)
        label_name = request.POST.get("label_name")
        label_color = request.POST.get("label_color")

        if label_name and label_color:
            MetaKanbanTaskLabel.objects.create(
                board=board, label_name=label_name, label_color=label_color, created_by_user=request.user
            )
            messages.success(request, "Label created successfully.")
        else:
            messages.error(request, "Both label name and color are required.")

        return redirect("metakanban:label_list", board_id=board_id)
