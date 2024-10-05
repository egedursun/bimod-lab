#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: reload_backup_views.py
#  Last Modified: 2024-10-01 14:26:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:37
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: reload_backup_views.py
#  Last Modified: 2024-09-30 14:37:21
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-30 14:37:28
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@bimod.io.
#
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from apps._services.data_backups.data_backup_executor import DataBackupExecutor
from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.data_backups.models import DataBackup
from apps.user_permissions.utils import PermissionNames


class ReloadBackupView(LoginRequiredMixin, View):
    def post(self, request, backup_id, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - RESTORE_DATA_BACKUPS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.RESTORE_DATA_BACKUPS):
            messages.error(self.request, "You do not have permission to restore backups.")
            return redirect('data_backups:manage')
        ##############################

        # Get the backup object by id
        backup = get_object_or_404(DataBackup, id=backup_id)

        # Get the password for restoration (for example, from a form field)
        password = request.POST.get('backup_password')  # Ensure this field is in your form

        try:
            # Use the executor to restore the backup
            result = DataBackupExecutor.restore(backup_object=backup, password=password)

            if result is None:
                # Restoration was successful
                messages.success(request, f"Backup '{backup.backup_name}' has been successfully reloaded.")
            else:
                # Handle the case where the restoration failed due to incorrect password or another issue
                messages.error(request, result)

        except Exception as e:
            # Handle any exceptions that occur during reloading
            messages.error(request, f"An error occurred while trying to reload the backup: {str(e)}")

        return redirect('data_backups:manage')
