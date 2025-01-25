#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: chrome_extension_connection_page_views.py
#  Last Modified: 2024-12-23 09:37:44
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-23 09:37:45
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
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.views.generic import (
    TemplateView
)

from apps.assistants.models import Assistant
from apps.browser_extensions.models import ChromeExtensionConnection
from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)
from apps.organization.models import Organization

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import (
    TemplateLayout
)

logger = logging.getLogger(__name__)


class BrowserExtensionsView_ChromeExtensionConnectionPage(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_BROWSER_EXTENSION_GOOGLE_APPS_CONNECTIONS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.LIST_BROWSER_EXTENSION_GOOGLE_APPS_CONNECTIONS
        ):
            messages.error(
                self.request,
                "You do not have permission to list Browser Extension Google Chrome Connections."
            )
            return context
        ##############################

        try:
            connections = ChromeExtensionConnection.objects.filter(
                owner_user=self.request.user
            )

            user_orgs = Organization.objects.filter(
                users__in=[self.request.user]
            )

            context['assistants'] = Assistant.objects.filter(
                organization__in=user_orgs
            )

            paginator = Paginator(connections, 10)
            page = self.request.GET.get('page')

            try:
                paginated_connections = paginator.page(page)

            except PageNotAnInteger:
                paginated_connections = paginator.page(1)

            except EmptyPage:
                paginated_connections = paginator.page(paginator.num_pages)

            context['connections'] = paginated_connections

        except Exception as e:
            messages.error(self.request, "An error occurred while retrieving connections.")

            context['connections'] = []

        return context
