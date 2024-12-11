#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_data_backup_views.py
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
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging

from django.contrib import messages

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.shortcuts import (
    redirect,
    get_object_or_404
)

from django.views import View

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.data_backups.models import DataBackup

from apps.user_permissions.utils import (
    PermissionNames
)

logger = logging.getLogger(__name__)


class DataBackupView_BackupDelete(LoginRequiredMixin, View):
    def post(
        self,
        request,
        backup_id,
        *args,
        **kwargs
    ):

        ##############################
        # PERMISSION CHECK FOR - DELETE_DATA_BACKUPS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_DATA_BACKUPS
        ):
            messages.error(request, "You do not have permission to delete backups.")
            return redirect('data_backups:manage')
        ##############################

        backup = get_object_or_404(
            DataBackup,
            id=backup_id
        )

        try:
            backup.delete()

            logger.info(f"User: {request.user} - Backup: {backup.backup_name} - Deleted.")
            messages.success(request, f"The backup '{backup.backup_name}' was deleted successfully.")

        except Exception as e:
            messages.error(request, f"An error occurred while trying to delete the backup: {str(e)}")

        logger.error(f"User: {request.user} - Backup: {backup.backup_name} - Deletion failed.")

        return redirect('data_backups:manage')
