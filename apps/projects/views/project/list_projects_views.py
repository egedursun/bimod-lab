#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_projects_views.py
#  Last Modified: 2024-10-24 22:02:15
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-24 22:02:16
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

from apps.projects.models import ProjectItem

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout


class ProjectsView_ProjectList(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_PROJECTS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.LIST_PROJECTS
        ):
            messages.error(self.request, "You do not have permission to list projects.")
            return context
        ##############################

        context['org_projects'] = {
            org: ProjectItem.objects.filter(
                organization=org
            ) for org in Organization.objects.filter(
                users__in=[
                    self.request.user
                ]
            )
        }

        return context
