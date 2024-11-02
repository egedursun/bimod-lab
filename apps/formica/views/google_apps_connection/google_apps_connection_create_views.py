#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: google_apps_connection_create_views.py
#  Last Modified: 2024-11-02 14:57:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-02 19:38:51
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
from django.shortcuts import redirect, get_object_or_404
from django.views import View

from apps.assistants.models import Assistant
from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.formica.models import FormicaGoogleAppsConnection
from apps.formica.utils import generate_google_apps_connection_api_key
from apps.user_permissions.utils import PermissionNames


class FormicaView_GoogleAppsConnectionCreate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - ADD_FORMICA_GOOGLE_APPS_CONNECTIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_FORMICA_GOOGLE_APPS_CONNECTIONS):
            messages.error(self.request, "You do not have permission to add Formica Google Apps Connections.")
            return redirect('formica:google_apps_connections_list')
        ##############################

        assistant_id = request.POST.get('assistant')
        if not assistant_id:
            messages.error(request, "Assistant field is required.")
            return redirect('formica:google_apps_connections_list')

        assistant = get_object_or_404(Assistant, id=assistant_id)

        connection, created = FormicaGoogleAppsConnection.objects.get_or_create(
            owner_user=request.user, formica_assistant=assistant,
            defaults={'connection_api_key': generate_google_apps_connection_api_key()}
        )

        if not created:
            messages.warning(request, "A connection for this model already exists. Please renew if necessary.")
        else:
            messages.success(request, "Connection successfully created.")

        return redirect('formica:google_apps_connections_list')
