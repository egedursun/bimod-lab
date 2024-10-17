#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_all_drafting_folders_views.py
#  Last Modified: 2024-10-17 12:36:01
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 12:36:02
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
from apps.drafting.models import DraftingFolder
from apps.user_permissions.utils import PermissionNames

logger = logging.getLogger(__name__)


class SettingsView_DeleteAllDraftingFolders(View, LoginRequiredMixin):
    def post(self, request, *args, **kwargs):
        user = request.user
        user_drafting_folders = DraftingFolder.objects.filter(organization__users__in=[user]).all()
        confirmation_field = request.POST.get('confirmation', None)
        if confirmation_field != 'CONFIRM DELETING ALL DRAFTING FOLDERS':
            logger.error(f"Invalid confirmation field: {confirmation_field}")
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL DRAFTING FOLDERS'.")
            return redirect('user_settings:settings')

        ##############################
        # PERMISSION CHECK FOR - DELETE_DRAFTING_FOLDERS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_DRAFTING_FOLDERS):
            messages.error(self.request, "You do not have permission to delete drafting folders.")
            return redirect('user_settings:settings')
        ##############################

        try:
            for drafting_folder in user_drafting_folders:
                drafting_folder.delete()
            logger.info(f"All drafting folders associated with User: {user.id} have been deleted.")
            messages.success(request, "All drafting folders associated with your account have been deleted.")
        except Exception as e:
            logger.error(f"Error deleting drafting folders: {e}")
            messages.error(request, f"Error deleting drafting folders: {e}")
        return redirect('user_settings:settings')
