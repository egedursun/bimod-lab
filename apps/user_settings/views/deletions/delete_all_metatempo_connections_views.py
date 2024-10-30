#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_all_metatempo_connections_views.py
#  Last Modified: 2024-10-30 19:18:09
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-30 19:18:09
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
from django.shortcuts import redirect
from django.views import View

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.metatempo.models import MetaTempoConnection
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames

logger = logging.getLogger(__name__)


class SettingsView_DeleteAllMetaTempoConnections(View, LoginRequiredMixin):
    def post(self, request, *args, **kwargs):
        user = request.user
        user_orgs = Organization.objects.filter(users__in=[user]).all()
        metatempo_connections = MetaTempoConnection.objects.filter(board__project__organization__in=user_orgs).all()
        confirmation_field = request.POST.get('confirmation', None)
        if confirmation_field != 'CONFIRM DELETING ALL METATEMPO CONNECTIONS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL METATEMPO CONNECTIONS'.")
            logger.error(f"Invalid confirmation field: {confirmation_field}")
            return redirect('user_settings:settings')

        ##############################
        # PERMISSION CHECK FOR - DELETE_METATEMPO_CONNECTION
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_METATEMPO_CONNECTION):
            messages.error(self.request, "You do not have permission to delete MetaTempo connections.")
            return redirect('user_settings:settings')
        ##############################

        try:
            for connection in metatempo_connections:
                connection.delete()
            messages.success(request, "All MetaTempo connections associated with your account have been deleted.")
            logger.info(f"All MetaTempo connections associated with User: {user.id} have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting MetaTempo connections: {e}")
            logger.error(f"Error deleting MetaTempo connections: {e}")
        return redirect('user_settings:settings')
