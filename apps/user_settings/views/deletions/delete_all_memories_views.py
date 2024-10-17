#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_all_memories_views.py
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
from apps.memories.models import AssistantMemory
from apps.user_permissions.utils import PermissionNames


logger = logging.getLogger(__name__)


class SettingsView_DeleteAllStandardMemories(View, LoginRequiredMixin):

    def post(self, request, *args, **kwargs):
        user = request.user
        user_std_memories = AssistantMemory.objects.filter(user=user).all()
        confirmation_field = request.POST.get('confirmation', None)
        if confirmation_field != 'CONFIRM DELETING ALL MEMORIES':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL MEMORIES'.")
            return redirect('user_settings:settings')

        ##############################
        # PERMISSION CHECK FOR - DELETE_ASSISTANT_MEMORIES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_ASSISTANT_MEMORIES):
            messages.error(self.request, "You do not have permission to delete assistant memories.")
            logger.error(f"User: {user.id} does not have permission to delete assistant memories.")
            return redirect('user_settings:settings')
        ##############################

        try:
            for std_memory in user_std_memories:
                std_memory.delete()
            messages.success(request, "All memories associated with your account have been deleted.")
            logger.info(f"All memories associated with User: {user.id} have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting memories: {e}")
            logger.error(f"Error deleting memories: {e}")
        return redirect('user_settings:settings')
