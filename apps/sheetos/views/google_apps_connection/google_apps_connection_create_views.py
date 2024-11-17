#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: google_apps_connection_create_views.py
#  Last Modified: 2024-10-31 19:25:44
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-31 19:25:46
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
from django.shortcuts import redirect, get_object_or_404
from django.views import View

from apps.assistants.models import Assistant
from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.sheetos.models import SheetosGoogleAppsConnection
from apps.sheetos.utils import generate_google_apps_connection_api_key
from apps.user_permissions.utils import PermissionNames

logger = logging.getLogger(__name__)


class SheetosView_GoogleAppsConnectionCreate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - ADD_SHEETOS_GOOGLE_APPS_CONNECTIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_SHEETOS_GOOGLE_APPS_CONNECTIONS):
            messages.error(self.request, "You do not have permission to add Sheetos Google Apps Connections.")
            return redirect('sheetos:google_apps_connections_list')
        ##############################

        assistant_id = request.POST.get('assistant')
        if not assistant_id:
            messages.error(request, "Assistant field is required.")
            return redirect('sheetos:google_apps_connections_list')

        assistant = get_object_or_404(Assistant, id=assistant_id)

        try:
            connection, created = SheetosGoogleAppsConnection.objects.get_or_create(
                owner_user=request.user, sheetos_assistant=assistant,
                defaults={'connection_api_key': generate_google_apps_connection_api_key()}
            )

            if not created:
                messages.warning(request, "A connection for this model already exists. Please renew if necessary.")
            else:
                messages.success(request, "Connection successfully created.")
        except Exception as e:
            logger.error(f"An error occurred while creating the Sheetos Google Apps Connection: {str(e)}")
            messages.error(request, f"An error occurred while creating the Sheetos Google Apps Connection: {str(e)}")
            return redirect('sheetos:google_apps_connections_list')

        logger.info(f"Sheetos Google Apps Connection was created by User: {request.user.id}.")
        return redirect('sheetos:google_apps_connections_list')
