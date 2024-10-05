#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: delete_browser_connection_views.py
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
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.datasource_browsers.models import DataSourceBrowserConnection
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DeleteBrowserConnectionView(LoginRequiredMixin, TemplateView):
    """
    Handles the deletion of a data source browser connection.

    This view allows users with the appropriate permissions to delete a browser connection. It ensures that the user has the necessary permissions before performing the deletion.

    Methods:
        get_context_data(self, **kwargs): Adds the browser connection to be deleted to the context for confirmation.
        post(self, request, *args, **kwargs): Deletes the browser connection if the user has the required permissions.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['browser_connection'] = get_object_or_404(DataSourceBrowserConnection, pk=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - DELETE_WEB_BROWSERS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_WEB_BROWSERS):
            messages.error(self.request, "You do not have permission to delete web browsers.")
            return redirect('datasource_browsers:list')
        ##############################

        browser_connection = get_object_or_404(DataSourceBrowserConnection, pk=self.kwargs['pk'])
        browser_connection.delete()
        messages.success(request, 'Browser Connection deleted successfully.')
        print("[DeleteBrowserConnectionView.post] Browser Connection deleted successfully.")
        return redirect('datasource_browsers:list')
