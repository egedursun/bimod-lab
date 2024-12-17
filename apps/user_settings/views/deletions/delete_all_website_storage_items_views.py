#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_all_website_storage_items_views.py
#  Last Modified: 2024-12-07 20:03:09
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-07 20:03:10
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
    DataSourceWebsiteStorageItem
)

from apps.user_permissions.utils import (
    PermissionNames
)

logger = logging.getLogger(__name__)


class SettingsView_DeleteAllWebsiteStorageItems(View, LoginRequiredMixin):

    def post(self, request, *args, **kwargs):
        user = request.user

        user_website_storage_items = DataSourceWebsiteStorageItem.objects.filter(
            storage__assistant__organization__users__in=[user]
        ).all()

        confirmation_field = request.POST.get('confirmation', None)

        if confirmation_field != 'CONFIRM DELETING ALL WEBSITE STORAGE ITEMS':
            messages.error(
                request,
                "Invalid confirmation field. Please confirm the deletion by typing "
                "exactly 'CONFIRM DELETING ALL WEBSITE STORAGE ITEMS'."
            )

            logger.error(f"Invalid confirmation field: {confirmation_field}")

            return redirect('user_settings:settings')

        ##############################
        # PERMISSION CHECK FOR - DELETE_WEBSITE_ITEMS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_WEBSITE_ITEMS
        ):
            messages.error(self.request, "You do not have permission to delete website storage items.")

            return redirect('user_settings:settings')
        ##############################

        try:
            for website_storage_item in user_website_storage_items:
                website_storage_item.delete()

            logger.info(f"All website storage items associated with User: {user.id} have been deleted.")
            messages.success(request, "All website storage items associated with your account have been deleted.")

        except Exception as e:
            logger.error(f"Error deleting website storage items: {e}")
            messages.error(request, f"Error deleting website storage items: {e}")

        return redirect('user_settings:settings')
