#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: datasource_website_storage_admin.py
#  Last Modified: 2024-12-07 20:33:11
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-07 20:33:11
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.contrib import admin

from apps.datasource_website.models import DataSourceWebsiteStorageConnection

from apps.datasource_website.utils import (
    DATASOURCE_WEBSITE_STORAGE_CONNECTION_ADMIN_LIST,
    DATASOURCE_WEBSITE_STORAGE_CONNECTION_ADMIN_FILTER,
    DATASOURCE_WEBSITE_STORAGE_CONNECTION_ADMIN_SEARCH
)


@admin.register(DataSourceWebsiteStorageConnection)
class DataSourceWebsiteStorageConnectionAdmin(admin.ModelAdmin):
    list_display = DATASOURCE_WEBSITE_STORAGE_CONNECTION_ADMIN_LIST
    list_filter = DATASOURCE_WEBSITE_STORAGE_CONNECTION_ADMIN_FILTER
    search_fields = DATASOURCE_WEBSITE_STORAGE_CONNECTION_ADMIN_SEARCH

    ordering = (
        '-created_at',
    )
