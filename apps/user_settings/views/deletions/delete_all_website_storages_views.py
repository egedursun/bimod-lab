#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_all_website_storages_views.py
#  Last Modified: 2024-12-07 20:03:00
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-07 20:03:00
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

from apps.datasource_website.models import (
    DataSourceWebsiteStorageConnection
)

from apps.user_permissions.utils import (
    PermissionNames
)

logger = logging.getLogger(__name__)


class SettingsView_DeleteAllWebsiteStorages(View, LoginRequiredMixin):

    def post(self, request, *args, **kwargs):
        user = request.user
        user_website_storages = DataSourceWebsiteStorageConnection.objects.filter(
            assistant__organization__users__in=[user]
        ).all()

        confirmation_field = request.POST.get('confirmation', None)

        if confirmation_field != 'CONFIRM DELETING ALL WEBSITE STORAGES':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL WEBSITE STORAGES'.")
            logger.error(f"Invalid confirmation field: {confirmation_field}")

            return redirect('user_settings:settings')

        ##############################
        # PERMISSION CHECK FOR - DELETE_WEBSITE_STORAGES
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_WEBSITE_STORAGES
        ):
            messages.error(self.request, "You do not have permission to delete website storages.")

            return redirect('user_settings:settings')
        ##############################

        try:
            for website_storage in user_website_storages:
                website_storage.delete()

            logger.info(f"All website storages associated with User: {user.id} have been deleted.")
            messages.success(request, "All website storages associated with your account have been deleted.")

        except Exception as e:
            logger.error(f"Error deleting website storages: {e}")
            messages.error(request, f"Error deleting website storages: {e}")

        return redirect('user_settings:settings')
