#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: confirm_delete_website_storage_connection_views.py
#  Last Modified: 2024-12-07 19:40:17
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-07 19:40:17
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
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.datasource_website.models import (
    DataSourceWebsiteStorageConnection
)

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class DataSourceWebsiteView_StorageConfirmDelete(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        connection_item = DataSourceWebsiteStorageConnection.objects.get(
            id=self.kwargs.get("pk")
        )

        if not connection_item:
            logger.error("Website storage connection not found.")
            messages.error(self.request, "Website storage connection not found.")

            return redirect("datasource_website:storage_list")

        context["connection"] = connection_item

        return context

    def post(
        self,
        request,
        *args,
        **kwargs
    ):
        ##############################
        # PERMISSION CHECK FOR - DELETE_WEBSITE_STORAGES
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_WEBSITE_STORAGES
        ):
            messages.error(self.request, "You do not have permission to delete website storage connections.")
            return redirect("datasource_website:storage_list")
        ##############################

        try:

            deletion_id = self.kwargs.get("pk")

            deletion_item = DataSourceWebsiteStorageConnection.objects.get(
                id=deletion_id
            )

            if not deletion_item:
                messages.error(self.request, "Website storage connection not found.")

                return redirect("datasource_website:storage_list")

            deletion_item.delete()

        except Exception as e:
            logger.error(f"Error: {e}")
            messages.error(self.request, "An error occurred while deleting the website storage connection.")

            return redirect("datasource_website:storage_list")

        messages.success(self.request, "Website storage connection has been successfully deleted.")

        return redirect("datasource_website:storage_list")
