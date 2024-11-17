#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: google_apps_connection_manage_views.py
#  Last Modified: 2024-10-31 03:23:26
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-31 03:23:26
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

from apps.assistants.models import Assistant
from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.drafting.models import DraftingGoogleAppsConnection
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DraftingView_GoogleAppsConnectionList(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_DRAFTING_GOOGLE_APPS_CONNECTIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_DRAFTING_GOOGLE_APPS_CONNECTIONS):
            messages.error(self.request, "You do not have permission to list Drafting Google Apps Connections.")
            return context
        ##############################

        try:
            context['connections'] = DraftingGoogleAppsConnection.objects.filter(owner_user=self.request.user)
            user_orgs = Organization.objects.filter(users__in=[self.request.user])
            context['assistants'] = Assistant.objects.filter(organization__in=user_orgs)
        except Exception as e:
            messages.error(self.request, 'An error occurred while getting assistants.')
            return context

        return context
