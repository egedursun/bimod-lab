#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_boards_views.py
#  Last Modified: 2024-10-26 23:43:29
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-26 23:43:30
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
from apps.metakanban.models import MetaKanbanBoard
from apps.organization.models import Organization
from apps.projects.models import ProjectItem
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class MetaKanbanView_BoardList(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_METAKANBAN_BOARD
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_METAKANBAN_BOARD):
            messages.error(self.request, "You do not have permission to list kanban boards.")
            return context
        ##############################

        user_orgs = Organization.objects.filter(users__in=[self.request.user])
        org_projects_boards = {}
        for org in user_orgs:
            projects = ProjectItem.objects.filter(organization=org)
            org_projects_boards[org] = {}
            for project in projects:
                boards = MetaKanbanBoard.objects.filter(project=project)
                org_projects_boards[org][project] = boards

        context['org_projects_boards'] = org_projects_boards
        return context
