#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: confirm_delete_board_column.py
#  Last Modified: 2024-10-26 23:44:53
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-26 23:45:43
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
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.metakanban.models import MetaKanbanStatusColumn
from apps.user_permissions.utils import PermissionNames


class MetaKanbanView_ColumnConfirmDelete(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        column_id = request.POST.get("column_id")
        column = get_object_or_404(MetaKanbanStatusColumn, id=column_id)
        board_id = column.board.id
        column_name = column.column_name

        ##############################
        # PERMISSION CHECK FOR - DELETE_METAKANBAN_COLUMN
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_METAKANBAN_COLUMN):
            messages.error(self.request, "You do not have permission to delete a kanban column.")
            return redirect('metakanban:board_detail', board_id=board_id)
        ##############################

        with transaction.atomic():
            column.delete()
            self.reorder_columns(board_id)

        messages.success(request, f'Column "{column_name}" deleted successfully.')
        return redirect("metakanban:board_detail", board_id=board_id)

    def reorder_columns(self, board_id):
        columns = MetaKanbanStatusColumn.objects.filter(board_id=board_id).order_by("position_id")
        for index, column in enumerate(columns):
            if column.position_id != index:
                column.position_id = index
                column.save()
