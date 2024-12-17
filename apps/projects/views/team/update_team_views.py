#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: update_team_views.py
#  Last Modified: 2024-10-24 22:02:39
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-24 22:02:40
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

from django.shortcuts import (
    get_object_or_404,
    redirect
)

from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.organization.models import (
    Organization
)

from apps.projects.models import (
    ProjectTeamItem,
    ProjectItem
)

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class ProjectsView_TeamUpdate(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        team_id = self.kwargs.get('pk')

        team = get_object_or_404(
            ProjectTeamItem,
            pk=team_id
        )

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

        context['users'] = list(
            set(
                orgs_users
            )
        )
        context['team'] = team

        context['selected_team_members'] = team.team_members.all()

        return context

    def post(self, request, *args, **kwargs):
        team_id = self.kwargs.get('pk')

        ##############################
        # PERMISSION CHECK FOR - UPDATE_TEAMS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.UPDATE_TEAMS
        ):
            messages.error(self.request, "You do not have permission to update project teams.")
            return redirect('projects:team_list')
        ##############################

        team = get_object_or_404(
            ProjectTeamItem,
            pk=team_id
        )

        team_name = request.POST.get("team_name")
        project_id = request.POST.get("project")
        description = request.POST.get("team_description")
        team_lead_id = request.POST.get("team_lead")
        members = request.POST.getlist("team_members")

        if (
            not team_name or
            not project_id or
            not team_lead_id
        ):
            messages.error(request, "Team name, project, and team lead are required fields.")

            return redirect(
                "projects:team_update",
                pk=team_id
            )

        try:
            project = ProjectItem.objects.get(
                id=project_id
            )

            team_lead = User.objects.get(
                id=team_lead_id
            )

            team.team_name = team_name
            team.project = project
            team.team_description = description
            team.team_lead = team_lead

            team.save()

            team.team_members.set(
                User.objects.filter(
                    id__in=members
                )
            )

        except Exception as e:
            messages.error(request, f"An error occurred while updating the Team: {str(e)}")

            return redirect("projects:team_list")

        messages.success(request, f"Team '{team_name}' has been updated successfully.")
        logger.info(f"Team updated: {team.id}")

        return redirect("projects:team_list")
