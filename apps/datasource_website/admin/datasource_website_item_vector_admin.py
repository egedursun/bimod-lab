#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: datasource_website_item_vector_admin.py
#  Last Modified: 2024-12-07 20:33:01
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-07 20:33:02
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

from apps.datasource_website.models import WebsiteItemChunkVectorData

from apps.datasource_website.utils import (
    DATASOURCE_WEBSITE_ITEM_CHUNK_VECTOR_DATA_ADMIN_LIST,
    DATASOURCE_WEBSITE_ITEM_CHUNK_VECTOR_DATA_ADMIN_FILTER,
    DATASOURCE_WEBSITE_ITEM_CHUNK_VECTOR_DATA_ADMIN_SEARCH
)


@admin.register(WebsiteItemChunkVectorData)
class WebsiteItemChunkVectorDataAdmin(admin.ModelAdmin):
    list_display = DATASOURCE_WEBSITE_ITEM_CHUNK_VECTOR_DATA_ADMIN_LIST
    search_fields = DATASOURCE_WEBSITE_ITEM_CHUNK_VECTOR_DATA_ADMIN_SEARCH
    list_filter = DATASOURCE_WEBSITE_ITEM_CHUNK_VECTOR_DATA_ADMIN_FILTER

    ordering = (
        '-created_at',
    )
