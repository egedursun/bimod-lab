#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_all_data_backups_views.py
#  Last Modified: 2024-10-17 12:48:39
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 12:48:40
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

from apps.data_backups.models import DataBackup

from apps.user_permissions.utils import (
    PermissionNames
)

logger = logging.getLogger(__name__)


class SettingsView_DeleteAllDataBackups(View, LoginRequiredMixin):
    def post(self, request, *args, **kwargs):
        user = request.user

        user_data_backups = DataBackup.objects.filter(
            organization__users__in=[user]
        ).all()

        confirmation_field = request.POST.get('confirmation', None)

        if confirmation_field != 'CONFIRM DELETING ALL DATA BACKUPS':
            logger.error(f"Invalid confirmation field: {confirmation_field}")
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL DATA BACKUPS'.")

            return redirect('user_settings:settings')

        ##############################
        # PERMISSION CHECK FOR - DELETE_DATA_BACKUPS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_DATA_BACKUPS
        ):
            messages.error(self.request, "You do not have permission to delete data backups.")
            return redirect('user_settings:settings')
        ##############################

        try:
            for data_backup in user_data_backups:
                data_backup.delete()

            logger.info(f"All data backups associated with User: {user.id} have been deleted.")
            messages.success(request, "All data backups associated with your account have been deleted.")

        except Exception as e:
            logger.error(f"Error deleting data backups: {e}")
            messages.error(request, f"Error deleting data backups: {e}")

        return redirect('user_settings:settings')
