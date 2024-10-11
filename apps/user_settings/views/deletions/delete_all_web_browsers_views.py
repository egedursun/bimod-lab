#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: delete_all_web_browsers_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:40
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.datasource_browsers.models import DataSourceBrowserConnection
from apps.user_permissions.utils import PermissionNames


class SettingsView_DeleteAllBrowsers(View, LoginRequiredMixin):

    def post(self, request, *args, **kwargs):
        user = request.user
        user_web_browsers = DataSourceBrowserConnection.objects.filter(assistant__organization__users__in=[user]).all()
        confirmation_field = request.POST.get('confirmation', None)
        if confirmation_field != 'CONFIRM DELETING ALL WEB BROWSERS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL WEB BROWSERS'.")
            return redirect('user_settings:settings')

        ##############################
        # PERMISSION CHECK FOR - DELETE_WEB_BROWSERS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_WEB_BROWSERS):
            messages.error(self.request, "You do not have permission to delete web browsers.")
            return redirect('user_settings:settings')
        ##############################

        try:
            for web_browser in user_web_browsers:
                web_browser.delete()
            messages.success(request, "All web browsers associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting web browsers: {e}")
        return redirect('user_settings:settings')
