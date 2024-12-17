#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_metatempo_connections_views.py
#  Last Modified: 2024-10-28 20:29:23
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-28 20:29:24
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
    MetaTempoConnection
)

from apps.organization.models import Organization
from apps.projects.models import ProjectItem

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout


class MetaTempoView_ConnectionList(LoginRequiredMixin, TemplateView):
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

        user = self.request.user
        org_projects_connections = {}

        organizations = Organization.objects.filter(
            users__in=[user]
        )

        for organization in organizations:
            projects = ProjectItem.objects.filter(
                organization=organization
            )

            project_connections = {}

            for project in projects:
                connections = MetaTempoConnection.objects.filter(
                    board__project=project
                )

                project_connections[project] = connections

            org_projects_connections[organization] = project_connections

        context['org_projects_connections'] = org_projects_connections

        return context
