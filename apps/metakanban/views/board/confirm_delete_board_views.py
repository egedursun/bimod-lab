#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: confirm_delete_board_views.py
#  Last Modified: 2024-10-26 23:44:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-26 23:44:11
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

from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.metakanban.models import MetaKanbanBoard

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout


class MetaKanbanView_BoardConfirmDelete(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        board_id = self.kwargs.get("board_id")

        context['board'] = get_object_or_404(
            MetaKanbanBoard,
            id=board_id
        )

        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - DELETE_METAKANBAN_BOARD
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_METAKANBAN_BOARD
        ):
            messages.error(self.request, "You do not have permission to delete a kanban board.")
            return redirect('metakanban:board_list')
        ##############################

        board_id = self.kwargs.get("board_id")

        board = get_object_or_404(
            MetaKanbanBoard,
            id=board_id
        )

        try:
            board_title = board.title

            board.delete()

        except Exception as e:
            messages.error(request, f'Error deleting kanban board: {e}')

            return redirect('metakanban:board_list')

        messages.success(request, f'The kanban board "{board_title}" was deleted successfully.')

        return redirect("metakanban:board_list")
