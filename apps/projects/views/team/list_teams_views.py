#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_teams_views.py
#  Last Modified: 2024-10-24 22:02:32
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-24 22:02:32
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

from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.organization.models import (
    Organization
)

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout


class ProjectsView_TeamList(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_TEAMS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.LIST_TEAMS
        ):
            messages.error(self.request, "You do not have permission to list project teams.")
            return context
        ##############################

        user_orgs = Organization.objects.filter(
            users__in=[self.request.user]
        )

        org_projects_teams = {}

        for org in user_orgs:
            projects = org.projectitem_set.all()
            project_teams = {}

            for project in projects:
                project_teams[project] = project.project_teams.all()

            org_projects_teams[org] = project_teams

        context['org_projects_teams'] = org_projects_teams

        return context
