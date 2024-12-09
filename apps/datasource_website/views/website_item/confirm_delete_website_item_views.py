#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: confirm_delete_website_item_views.py
#  Last Modified: 2024-12-07 19:41:21
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-07 19:41:21
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
    DataSourceWebsiteStorageItem
)
from apps.datasource_website.tasks import (
    handle_delete_website_item
)

from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class DataSourceWebsiteView_WebsiteItemConfirmDelete(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        item_id = self.kwargs.get("pk")

        item = DataSourceWebsiteStorageItem.objects.get(
            id=item_id
        )

        if not item:
            logger.error(f"Item not found with ID: {item_id}")
            messages.error(self.request, "Website item not found.")
            return redirect("datasource_website:website_item_list")

        context["item"] = item
        return context

    def post(
        self,
        request,
        *args,
        **kwargs
    ):
        ##############################
        # PERMISSION CHECK FOR - DELETE_WEBSITE_ITEMS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_WEBSITE_ITEMS
        ):
            messages.error(self.request, "You do not have permission to delete website items.")
            return redirect("datasource_website:website_item_list")
        ##############################

        try:

            deletion_id = self.kwargs.get("pk")

            deletion_item = DataSourceWebsiteStorageItem.objects.get(
                id=deletion_id
            )

            if not deletion_item:
                messages.error(self.request, "Website item not found.")
                return redirect("datasource_website:website_item_list")

            success = handle_delete_website_item(item=deletion_item)

            if success is False:
                messages.error(self.request, "An error occurred while deleting the website item.")
                return redirect("datasource_website:website_item_list")

        except Exception as e:
            logger.error(f"Error: {e}")
            messages.error(self.request, "An error occurred while deleting the website item.")

            return redirect("datasource_website:website_item_list")

        messages.success(self.request, "Website item has been successfully deleted.")

        return redirect("datasource_website:website_item_list")
