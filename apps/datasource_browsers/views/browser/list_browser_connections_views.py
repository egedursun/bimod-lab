#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#
import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_browsers.models import DataSourceBrowserConnection
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


logger = logging.getLogger(__name__)


class BrowserView_BrowserList(LoginRequiredMixin, TemplateView):
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

        cs_by_orgs = {}
        agents = Assistant.objects.filter(organization__in=context_user.organizations.filter(users__in=[context_user]))
        for agent in agents:
            org = agent.organization
            if org not in cs_by_orgs:
                cs_by_orgs[org] = {}
            if agent not in cs_by_orgs[org]:
                cs_by_orgs[org][agent] = []

            cs = DataSourceBrowserConnection.objects.filter(assistant=agent)
            cs_by_orgs[org][agent].extend(cs)

        logger.info(f"Browser Connections were listed.")
        context['connections_by_organization'] = cs_by_orgs
        context['user'] = context_user
        return context
