#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: delete_data_backup_views.py
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
#  File: delete_data_backup_views.py
#  Last Modified: 2024-09-30 13:03:25
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-30 13:03:26
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
from django.shortcuts import redirect, get_object_or_404
from django.views import View

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.data_backups.models import DataBackup
from apps.user_permissions.utils import PermissionNames


class DeleteDataBackupView(LoginRequiredMixin, View):
    def post(self, request, backup_id, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - DELETE_DATA_BACKUPS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_DATA_BACKUPS):
            messages.error(request, "You do not have permission to delete backups.")
            return redirect('data_backups:manage')
        ##############################

        # Get the backup object by id
        backup = get_object_or_404(DataBackup, id=backup_id)

        try:
            # Attempt to delete the backup
            backup.delete()
            messages.success(request, f"The backup '{backup.backup_name}' was deleted successfully.")
        except Exception as e:
            # Handle any exceptions that occur during deletion
            messages.error(request, f"An error occurred while trying to delete the backup: {str(e)}")

        return redirect('data_backups:manage')
