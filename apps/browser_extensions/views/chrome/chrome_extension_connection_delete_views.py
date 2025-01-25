#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: chrome_extension_connection_delete_views.py
#  Last Modified: 2024-12-23 09:53:46
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-23 09:53:48
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

from django.shortcuts import (
    redirect,
    get_object_or_404
)

from django.views import View

from apps.browser_extensions.models import (
    ChromeExtensionConnection
)

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.user_permissions.utils import (
    PermissionNames
)


class BrowserExtensionsView_ChromeExtensionConnectionDelete(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        connection_id = kwargs.get('pk')

        ##############################
        # PERMISSION CHECK FOR - DELETE_BROWSER_EXTENSION_GOOGLE_APPS_CONNECTIONS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_BROWSER_EXTENSION_GOOGLE_APPS_CONNECTIONS
        ):
            messages.error(self.request, "You do not have permission to delete Browser Extension Google Chrome Connections.")
            return redirect('browser_extensions:google_apps_connections_list')
        ##############################

        connection = get_object_or_404(
            ChromeExtensionConnection,
            id=connection_id,
            owner_user=request.user
        )

        try:
            connection.delete()

        except Exception as e:
            messages.error(request, "An error occurred while deleting the connection.")

            return redirect('browser_extensions:google_apps_connections_list')

        messages.success(request, "Connection successfully deleted.")

        return redirect('browser_extensions:google_apps_connections_list')
