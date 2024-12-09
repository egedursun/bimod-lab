#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_website_item_views.py
#  Last Modified: 2024-12-07 19:40:58
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-07 19:40:58
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
    DataSourceWebsiteStorageConnection,
    DataSourceWebsiteStorageItem
)
from apps.datasource_website.tasks import crawl_and_index_website_item

from apps.user_permissions.utils import PermissionNames
from config.settings import MAX_WEBSITE_ITEMS_PER_STORAGE

logger = logging.getLogger(__name__)


class DataSourceWebsiteView_WebsiteItemCreate(LoginRequiredMixin, View):

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
        # PERMISSION CHECK FOR - ADD_WEBSITE_ITEMS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.ADD_WEBSITE_ITEMS
        ):
            messages.error(self.request, "You do not have permission to add website items.")
            return redirect("datasource_website:website_item_list")
        ##############################

        try:

            storage_id = request.POST.get('storage_id')
            storage = DataSourceWebsiteStorageConnection.objects.get(id=storage_id)

            n_website_items = storage.storage_items.count()

            if n_website_items > MAX_WEBSITE_ITEMS_PER_STORAGE:
                messages.error(
                    request,
                    f'Assistant has reached the maximum number of website items ({MAX_WEBSITE_ITEMS_PER_STORAGE}).'
                )

                return redirect('datasource_website:website_item_list')

            if storage is None:
                messages.error(request, "Website storage connection not found.")
                return redirect('datasource_website:website_item_list')

            website_url = request.POST.get('website_url')
            crawling_methodology = request.POST.get('crawling_methodology')

            new_website_item = DataSourceWebsiteStorageItem.objects.create(
                storage=storage,
                website_url=website_url,
                crawling_methodology=crawling_methodology,
                created_by_user=request.user,
            )

            # Crawl and index the website item.
            crawl_and_index_website_item(
                item_id=new_website_item.id,
                delete_previous=False
            )

        except Exception as e:
            logger.error("There was an error creating a new website item: %s" % str(e))
            messages.error(request, "There was an error creating a new website item.")

        messages.success(request, "Website item created successfully.")
        return redirect('datasource_website:website_item_list')
