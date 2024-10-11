#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: reload_backup_views.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:39
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from apps.core.data_backups.data_backup_executor import DataBackupExecutor
from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.data_backups.models import DataBackup
from apps.user_permissions.utils import PermissionNames


class DataBackupView_ReloadBackup(LoginRequiredMixin, View):
    def post(self, request, backup_id, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - RESTORE_DATA_BACKUPS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.RESTORE_DATA_BACKUPS):
            messages.error(self.request, "You do not have permission to restore backups.")
            return redirect('data_backups:manage')
        ##############################

        backup = get_object_or_404(DataBackup, id=backup_id)
        password = request.POST.get('backup_password')
        try:
            result = DataBackupExecutor.restore(backup_object=backup, password=password)
            if result is None:
                messages.success(request, f"Backup '{backup.backup_name}' has been successfully reloaded.")
            else:
                messages.error(request, result)
        except Exception as e:
            messages.error(request, f"An error occurred while trying to reload the backup: {str(e)}")
        return redirect('data_backups:manage')
