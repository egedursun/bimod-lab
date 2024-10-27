#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: move_column_views.py
#  Last Modified: 2024-10-27 02:28:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-27 02:28:14
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
import logging

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.metakanban.models import MetaKanbanStatusColumn
from apps.user_permissions.utils import PermissionNames

logger = logging.getLogger(__name__)


class MetaKanbanView_ColumnMove(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        board_id = request.POST.get("board_id")
        column_id = request.POST.get("column_id")
        direction = request.POST.get("direction")

        ##############################
        # PERMISSION CHECK FOR - MOVE_METAKANBAN_COLUMN
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.MOVE_METAKANBAN_COLUMN):
            messages.error(self.request, "You do not have permission to move a kanban column.")
            return redirect('metakanban:board_detail', board_id=board_id)
        ##############################

        try:
            column = get_object_or_404(MetaKanbanStatusColumn, id=column_id, board_id=board_id)
            old_position_id = column.position_id
            if direction == 'up' and old_position_id > 0:
                new_position_id = old_position_id - 1
            elif direction == 'down':
                new_position_id = old_position_id + 1
            else:
                messages.info(request, "Column is already at the specified position.")
                return redirect("metakanban:board_detail", board_id=board_id)

            with transaction.atomic():
                adjacent_column = MetaKanbanStatusColumn.objects.get(board_id=board_id, position_id=new_position_id)
                adjacent_column.position_id = old_position_id
                adjacent_column.save()
                column.position_id = new_position_id
                column.save()

            self.reorder_columns(board_id)
            messages.success(request, f'Column "{column.column_name}" moved {direction}.')

        except Exception as e:
            logger.error(f"Column could not be moved. Error: {str(e)}")
            messages.error(request, f"Column could not be moved. Error: {str(e)}")

        return redirect("metakanban:board_detail", board_id=board_id)

    def reorder_columns(self, board_id):
        columns = MetaKanbanStatusColumn.objects.filter(board_id=board_id).order_by("position_id")
        for index, column in enumerate(columns):
            if column.position_id != index:
                column.position_id = index
                column.save()
