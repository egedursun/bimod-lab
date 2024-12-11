#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: media_item_vector_admin.py
#  Last Modified: 2024-12-01 23:08:38
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-01 23:08:38
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

from apps.datasource_media_storages.models import (
    MediaItemVectorData
)

from apps.datasource_media_storages.utils import (
    MEDIA_ITEM_VECTOR_DATA_ADMIN_LIST,
    MEDIA_ITEM_VECTOR_DATA_ADMIN_FILTER,
    MEDIA_ITEM_VECTOR_DATA_ADMIN_SEARCH
)


@admin.register(MediaItemVectorData)
class MediaItemVectorDataAdmin(admin.ModelAdmin):
    list_display = MEDIA_ITEM_VECTOR_DATA_ADMIN_LIST
    search_fields = MEDIA_ITEM_VECTOR_DATA_ADMIN_SEARCH
    list_filter = MEDIA_ITEM_VECTOR_DATA_ADMIN_FILTER

    ordering = ('created_at',)
