#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: detail_board_views.py
#  Last Modified: 2024-10-26 23:43:38
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-26 23:43:45
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
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.metakanban.models import (MetaKanbanBoard, MetaKanbanStatusColumn, MetaKanbanTask,
                                    MetaKanbanTaskLabel)
from apps.metakanban.utils import META_KANBAN_TASK_PRIORITIES
from apps.projects.models import ProjectItem
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class MetaKanbanView_BoardDetail(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_METAKANBAN_BOARD
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_METAKANBAN_BOARD):
            messages.error(self.request, "You do not have permission to list kanban boards.")
            return context
        ##############################

        board_id = kwargs.get("board_id")
        board = MetaKanbanBoard.objects.get(id=board_id)

        context["board"] = MetaKanbanBoard.objects.get(id=board_id)
        context["columns"] = MetaKanbanStatusColumn.objects.filter(board_id=board_id).order_by("position_id")
        context["tasks"] = MetaKanbanTask.objects.filter(status_column__board_id=board_id)
        context["labels"] = MetaKanbanTaskLabel.objects.filter(board_id=board_id)
        context["priorities"] = META_KANBAN_TASK_PRIORITIES

        projects = ProjectItem.objects.filter(id=board.project.id).all()
        project_team_members = []
        for project in projects:
            teams = project.project_teams.all()
            for team in teams:
                project_team_members.extend(team.team_members.all())
        project_team_members = list(set(project_team_members))
        context["users"] = project_team_members
        return context
