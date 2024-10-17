#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_all_starred_messages_views.py
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
#   For permission inquiries, please contact: admin@Bimod.io.
#
import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.starred_messages.models import StarredMessage
from apps.user_permissions.utils import PermissionNames


logger = logging.getLogger(__name__)


class SettingsView_DeleteAllStarredMessages(View, LoginRequiredMixin):

    def post(self, request, *args, **kwargs):
        user = request.user
        user_starred_messages = StarredMessage.objects.filter(user=user).all()
        confirmation_field = request.POST.get('confirmation', None)
        if confirmation_field != 'CONFIRM DELETING ALL STARRED MESSAGES':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL STARRED MESSAGES'.")
            logger.error(f"Invalid confirmation field: {confirmation_field}")
            return redirect('user_settings:settings')

        ##############################
        # PERMISSION CHECK FOR - REMOVE_STARRED_MESSAGES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.REMOVE_STARRED_MESSAGES):
            messages.error(self.request, "You do not have permission to remove starred messages.")
            return redirect('user_settings:settings')
        ##############################

        try:
            for starred_message in user_starred_messages:
                starred_message.delete()
            messages.success(request, "All starred messages associated with your account have been deleted.")
            logger.info(f"All starred messages associated with User: {user.id} have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting starred messages: {e}")
            logger.error(f"Error deleting starred messages: {e}")
        return redirect('user_settings:settings')
