#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_team_views.py
#  Last Modified: 2024-10-24 22:02:21
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-24 22:02:22
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging

from django.contrib import messages

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.organization.models import (
    Organization
)

from apps.projects.models import (
    ProjectItem,
    ProjectTeamItem
)
from apps.user_permissions.utils import (
    PermissionNames
)

from config.settings import (
    MAX_TEAMS_PER_PROJECT
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class ProjectsView_TeamCreate(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        user_orgs = Organization.objects.filter(
            users__in=[self.request.user]
        )

        context['projects'] = ProjectItem.objects.filter(
            organization__in=user_orgs
        )

        orgs_users = []

        for org in user_orgs:
            org_users = org.users.all()
            orgs_users = orgs_users + list(org_users)

        orgs_users = list(set(orgs_users))
        context['users'] = orgs_users

        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - ADD_TEAMS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.ADD_TEAMS
        ):
            messages.error(self.request, "You do not have permission to add project teams.")
            return redirect('projects:team_list')
        ##############################

        team_name = request.POST.get("team_name")
        project_id = request.POST.get("project")
        description = request.POST.get("team_description")
        team_lead_id = request.POST.get("team_lead")
        members = request.POST.getlist("team_members")  # Capture selected members

        if (
            not team_name or
            not project_id or
            not team_lead_id
        ):
            messages.error(request, "Team name, project, and team lead are required fields.")

            return redirect("projects:team_create")

        try:
            project = ProjectItem.objects.get(
                id=project_id
            )

            team_lead = User.objects.get(
                id=team_lead_id
            )

            # check the number of project teams the project has

            n_project_teams = project.project_teams.count()

            if n_project_teams > MAX_TEAMS_PER_PROJECT:
                messages.error(
                    request,
                    f'Assistant has reached the maximum number of teams per project ({MAX_TEAMS_PER_PROJECT}).'
                )

                return redirect('projects:team_create')

            team = ProjectTeamItem.objects.create(
                team_name=team_name,
                project=project,
                team_description=description,
                team_lead=team_lead,
                created_by_user=request.user
            )

            team.team_members.set(
                User.objects.filter(
                    id__in=members
                )
            )

        except Exception as e:
            messages.error(request, f"An error occurred while creating the team: {str(e)}")

            return redirect("projects:team_create")

        messages.success(request, f"Team '{team_name}' has been created successfully.")
        logger.info(f"New team created: {team.id}")

        return redirect("projects:team_list")
