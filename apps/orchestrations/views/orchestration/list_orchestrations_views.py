#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: list_orchestrations_views.py
#  Last Modified: 2024-09-28 00:53:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:07:12
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.orchestrations.models import Maestro
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class OrchestrationListView(LoginRequiredMixin, TemplateView):
    """
    Displays a list of orchestrations within the Bimod.io platform.

    This view displays a list of orchestrations that the user has access to. It organizes the orchestrations
    by organization.
    """
    template_name = 'orchestrations/list_orchestrations.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_ORCHESTRATIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_ORCHESTRATIONS):
            messages.error(self.request, "You do not have permission to list orchestrations.")
            return context
        ##############################

        user_organizations = Organization.objects.filter(users__in=[self.request.user])
        orchestrations = Maestro.objects.filter(organization__in=user_organizations)

        # Organizing orchestrations by organization
        orchestrations_by_org = {}
        for org in user_organizations:
            orchestrations_by_org[org] = orchestrations.filter(organization=org)

        context['orchestrations_by_organization'] = orchestrations_by_org
        return context
