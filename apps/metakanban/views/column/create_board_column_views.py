#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_board_column.py
#  Last Modified: 2024-10-26 23:44:38
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-26 23:45:52
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

from django.db import (
    models,
    transaction
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
    MetaKanbanStatusColumn,
    MetaKanbanChangeLog
)

from apps.metakanban.utils import (
    MetaKanbanChangeLogActionTypes
)

from apps.user_permissions.utils import (
    PermissionNames
)


class MetaKanbanView_ColumnCreate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        board_id = request.POST.get("board_id")

        board = get_object_or_404(
            MetaKanbanBoard,
            id=board_id
        )

        ##############################
        # PERMISSION CHECK FOR - ADD_METAKANBAN_COLUMN
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.ADD_METAKANBAN_COLUMN
        ):
            messages.error(self.request, "You do not have permission to add a kanban column.")

            return redirect(
                'metakanban:board_detail',
                board_id=board_id
            )
        ##############################

        column_name = request.POST.get("column_name")
        position_id = request.POST.get("position_id")

        if (
            column_name and
            position_id is not None
        ):
            position_id = int(position_id)

            with transaction.atomic():
                MetaKanbanStatusColumn.objects.filter(
                    board=board,
                    position_id__gte=position_id
                ).update(
                    position_id=models.F(
                        "position_id"
                    ) + 1
                )
                MetaKanbanStatusColumn.objects.create(
                    board=board,
                    column_name=column_name,
                    position_id=position_id,
                    created_by_user=request.user
                )

            self.reorder_columns(
                board_id
            )

            messages.success(
                request,
                f'Column "{column_name}" created successfully at position {position_id}.'
            )
        else:
            messages.error(
                request,
                "Column name and position are required to create a new column."
            )

        try:
            MetaKanbanChangeLog.objects.create(
                board=board,
                action_type=MetaKanbanChangeLogActionTypes.Column.CREATE_COLUMN,
                action_details="A new column created for the board, with the name: " + column_name,
                change_by_user=request.user
            )

        except Exception as e:
            messages.error(request, "Column change log could not be created. Error: " + str(e))

        return redirect(
            "metakanban:board_detail",
            board_id=board_id
        )

    def reorder_columns(
        self,
        board_id
    ):
        columns = MetaKanbanStatusColumn.objects.filter(
            board_id=board_id
        ).order_by(
            "position_id"
        )

        for index, column in enumerate(columns):
            if column.position_id != index:
                column.position_id = index

                column.save()
