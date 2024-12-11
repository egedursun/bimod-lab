#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: refresh_website_item_views.py
#  Last Modified: 2024-12-07 19:41:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-07 19:41:10
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

from apps.datasource_website.tasks import (
    crawl_and_index_website_item
)

from apps.user_permissions.utils import (
    PermissionNames
)

logger = logging.getLogger(__name__)


class DataSourceWebsiteView_WebsiteItemRefresh(LoginRequiredMixin, View):

    def get(
        self,
        request,
        *args,
        **kwargs
    ):
        return self.post(request, *args, **kwargs)

    def post(
        self,
        request,
        *args,
        **kwargs
    ):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_WEBSITE_ITEMS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.UPDATE_WEBSITE_ITEMS
        ):
            messages.error(self.request, "You do not have permission to update website items.")
            return redirect("datasource_website:website_item_list")
        ##############################

        try:

            item_id = kwargs.get("pk")

            existing_website_item = DataSourceWebsiteStorageItem.objects.get(
                id=item_id
            )

            if not existing_website_item:
                logger.error("The website item does not exist.")
                messages.error(request, "The website item does not exist.")

                return redirect("datasource_website:website_item_list")

            # Crawl and index the website item.
            crawl_and_index_website_item(
                item_id=existing_website_item.id,
                delete_previous=True
            )

        except Exception as e:
            logger.error("There was an error while refreshing the website item: %s" % e)
            messages.error(request, "There was an error while refreshing the website item.")

            return redirect("datasource_website:website_item_list")

        messages.success(request, "The website item has been refreshed successfully.")

        return redirect("datasource_website:website_item_list")
