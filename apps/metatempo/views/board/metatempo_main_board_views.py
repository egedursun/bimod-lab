#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: metatempo_main_board_views.py
#  Last Modified: 2024-10-28 20:30:23
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-28 20:30:23
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

from apps.metatempo.models import (
    MetaTempoConnection,
    MetaTempoMemberLog,
    MetaTempoMemberLogDaily,
    MetaTempoProjectOverallLog
)

from apps.organization.models import Organization

from apps.projects.models import (
    ProjectItem,
    ProjectTeamItem
)

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout


class MetaTempoView_MainBoard(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_METATEMPO_CONNECTION
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.LIST_METATEMPO_CONNECTION
        ):
            messages.error(self.request, "You do not have permission to list MetaTempo Connections.")

            return context
        ##############################

        connection_id = self.kwargs.get('connection_id')

        connection = MetaTempoConnection.objects.get(
            id=connection_id
        )

        org_users = Organization.objects.filter(
            users__in=[self.request.user]
        )

        org_projects = ProjectItem.objects.filter(
            organization__in=org_users
        )

        org_users = []
        for project in org_projects:
            project: ProjectItem

            teams = project.project_teams.all()

            for team in teams:
                team: ProjectTeamItem
                team_users = team.team_members.all()

                org_users.extend(
                    team_users
                )

        org_users = list(
            set(
                org_users
            )
        )

        member_logs = MetaTempoMemberLog.objects.filter(
            metatempo_connection=connection
        ).order_by(
            '-timestamp'
        )

        daily_logs = MetaTempoMemberLogDaily.objects.filter(
            metatempo_connection=connection
        ).order_by(
            '-datestamp'
        )

        overall_logs = MetaTempoProjectOverallLog.objects.filter(
            metatempo_connection=connection
        ).order_by(
            '-datestamp'
        )

        context.update(
            {
                "connection": connection,
                "member_logs": member_logs,
                "daily_logs": daily_logs,
                "overall_logs": overall_logs,
                "users": org_users,
                "user_auth_key": self.request.user.profile.metatempo_tracking_auth_key,
                "connection_api_key": connection.connection_api_key,
            }
        )

        return context
