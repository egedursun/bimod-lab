#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_metakanban_board_logs_views.py
#  Last Modified: 2024-10-27 21:57:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-27 21:57:47
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
from django.core.paginator import Paginator
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.metakanban.models import MetaKanbanChangeLog, MetaKanbanBoard
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class MetaKanbanView_BoardLogList(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_METAKANBAN_BOARD
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_METAKANBAN_BOARD):
            messages.error(self.request, "You do not have permission to list kanban boards.")
            return context
        ##############################

        board_id = self.kwargs.get('board_id')
        board = MetaKanbanBoard.objects.get(id=board_id)

        logs_list = MetaKanbanChangeLog.objects.filter(board_id=board_id).order_by('-timestamp').all()
        paginator = Paginator(logs_list, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['board'] = board
        context['page_obj'] = page_obj
        return context
