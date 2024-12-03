#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_browsing_logs_views.py
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
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.datasource_browsers.models import (
    DataSourceBrowserConnection
)

from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class BrowserView_BrowserLogList(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_WEB_BROWSERS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.LIST_WEB_BROWSERS
        ):
            messages.error(self.request, "You do not have permission to list web browsers.")
            return context
        ##############################

        c_id = kwargs.get('pk')
        browser_c = get_object_or_404(DataSourceBrowserConnection, pk=c_id)

        try:
            context['browser_connection'] = browser_c
            logs = browser_c.logs.all()
            search_query = self.request.GET.get('search', '')

            if search_query:
                logs = logs.filter(
                    action__icontains=search_query
                ) | logs.filter(
                    html_content__icontains=search_query
                ) | logs.filter(
                    context_content__icontains=search_query
                ) | logs.filter(
                    log_content__icontains=search_query
                )

            paginator = Paginator(logs, 10)
            page_number = self.request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context['page_obj'] = page_obj
            context['search_query'] = search_query

        except Exception as e:
            logger.error(
                f"User: {self.request.user} - Browser Connection: {browser_c.name} - Browsing Logs List Error: {e}"
            )

            messages.error(self.request, 'An error occurred while listing Browsing Logs.')
            return context

        logger.info(f"User: {self.request.user} - Browser Connection: {browser_c.name} - Browsing Logs Listed.")
        return context
