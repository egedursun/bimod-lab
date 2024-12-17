#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_all_chats_views.py
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

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.shortcuts import redirect
from django.views import View

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.multimodal_chat.models import MultimodalChat

from apps.user_permissions.utils import (
    PermissionNames
)

logger = logging.getLogger(__name__)


class SettingsView_DeleteAllChats(View, LoginRequiredMixin):

    def post(self, request, *args, **kwargs):
        user = request.user

        user_chats = MultimodalChat.objects.filter(
            organization__users__in=[user]
        ).all()

        confirmation_field = request.POST.get('confirmation', None)

        if confirmation_field != 'CONFIRM DELETING ALL CHATS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL CHATS'.")
            logger.error(f"Invalid confirmation field: {confirmation_field}")

            return redirect('user_settings:settings')

        ##############################
        # PERMISSION CHECK FOR - REMOVE_CHATS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.REMOVE_CHATS
        ):
            messages.error(self.request, "You do not have permission to delete chats.")
            return redirect('user_settings:settings')
        ##############################

        try:
            for chat in user_chats:
                chat.delete()

            logger.info(f"All chat messages associated with User: {user.id} have been deleted.")
            messages.success(request, "All chat messages associated with your account have been deleted.")

        except Exception as e:
            logger.error(f"Error deleting chat messages: {e}")
            messages.error(request, f"Error deleting chat messages: {e}")

        return redirect('user_settings:settings')
