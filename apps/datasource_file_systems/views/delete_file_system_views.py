#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_file_system_views.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:46
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
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.datasource_file_systems.models import (
    DataSourceFileSystem
)

from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class FileSystemView_Delete(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - DELETE_FILE_SYSTEMS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_FILE_SYSTEMS
        ):
            messages.error(self.request, "You do not have permission to delete file system connections.")
            return redirect('datasource_file_systems:list')
        ##############################

        conn = get_object_or_404(
            DataSourceFileSystem,
            pk=kwargs['pk']
        )

        try:
            conn.delete()

        except Exception as e:
            logger.error(f"User: {request.user} - File System - Delete Error: {e}")
            messages.error(request, 'An error occurred while deleting the file system connection.')
            return redirect('datasource_file_systems:list')

        logger.info(f"[FileSystemView_Delete] File System Connection Deleted: {conn}")
        return redirect('datasource_file_systems:list')
