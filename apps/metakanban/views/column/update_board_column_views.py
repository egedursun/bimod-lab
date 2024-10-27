#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: update_board_column.py
#  Last Modified: 2024-10-26 23:44:46
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-26 23:46:02
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
from apps.metakanban.models import MetaKanbanStatusColumn
from apps.user_permissions.utils import PermissionNames


class MetaKanbanView_ColumnUpdate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        column_id = request.POST.get("column_id")
        column = get_object_or_404(MetaKanbanStatusColumn, id=column_id)

        ##############################
        # PERMISSION CHECK FOR - UPDATE_METAKANBAN_COLUMN
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_METAKANBAN_COLUMN):
            messages.error(self.request, "You do not have permission to update a kanban column.")
            return redirect('metakanban:board_detail', board_id=column.board.id)
        ##############################

        new_column_name = request.POST.get("column_name")
        if new_column_name:
            column.column_name = new_column_name
            column.save()
            messages.success(request, f'Column "{new_column_name}" updated successfully.')
        else:
            messages.error(request, "Column name cannot be empty.")
        return redirect("metakanban:board_detail", board_id=column.board.id)
