#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: list_browser_connections_views.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:46
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_browsers.models import DataSourceBrowserConnection
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class ListBrowserConnectionsView(LoginRequiredMixin, TemplateView):
    """
    Displays a list of browser connections associated with the user's assistants and organizations.

    This view retrieves all browser connections organized by organization and assistant, and displays them in a structured list.

    Methods:
        get_context_data(self, **kwargs): Retrieves the browser connections organized by organization and assistant, and adds them to the context.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - LIST_WEB_BROWSERS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_WEB_BROWSERS):
            messages.error(self.request, "You do not have permission to list web browsers.")
            return context
        ##############################

        connections_by_organization = {}
        assistants = Assistant.objects.filter(
            organization__in=context_user.organizations.filter(users__in=[context_user])
        )

        for assistant in assistants:
            organization = assistant.organization
            if organization not in connections_by_organization:
                connections_by_organization[organization] = {}
            if assistant not in connections_by_organization[organization]:
                connections_by_organization[organization][assistant] = []

            connections = DataSourceBrowserConnection.objects.filter(assistant=assistant)
            connections_by_organization[organization][assistant].extend(connections)

        context['connections_by_organization'] = connections_by_organization
        context['user'] = context_user
        print("[ListBrowserConnectionsView.get_context_data] Browser Connections listed successfully.")
        return context
