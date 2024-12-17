#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_all_video_generator_connections_views.py
#  Last Modified: 2024-10-17 12:46:02
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 12:46:27
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

from django.shortcuts import redirect
from django.views import View

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.user_permissions.utils import (
    PermissionNames
)

from apps.video_generations.models import (
    VideoGeneratorConnection
)

logger = logging.getLogger(__name__)


class SettingsView_DeleteAllVideoGeneratorConnections(View, LoginRequiredMixin):
    def post(self, request, *args, **kwargs):
        user = request.user

        user_connections = VideoGeneratorConnection.objects.filter(
            organization__users__in=[user]
        ).all()

        confirmation_field = request.POST.get('confirmation', None)

        if confirmation_field != 'CONFIRM DELETING ALL VIDEO GENERATOR CONNECTIONS':
            logger.error(f"Invalid confirmation field: {confirmation_field}")
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL VIDEO GENERATOR CONNECTIONS'.")

            return redirect('user_settings:settings')

        ##############################
        # PERMISSION CHECK FOR - DELETE_VIDEO_GENERATOR_CONNECTIONS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_VIDEO_GENERATOR_CONNECTIONS
        ):
            messages.error(self.request, "You do not have permission to delete video generator connections.")

            return redirect('user_settings:settings')
        ##############################

        try:
            for video_generator_connection in user_connections:
                video_generator_connection.delete()

            logger.info(f"All video generator connections associated with User: {user.id} have been deleted.")
            messages.success(request,
                             "All video generator connections associated with your account have been deleted.")

        except Exception as e:
            logger.error(f"Error deleting video generator connections: {e}")
            messages.error(request, f"Error deleting video generator connections: {e}")

        return redirect('user_settings:settings')
