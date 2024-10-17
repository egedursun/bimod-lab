#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: media_storage_admin.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:48
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
#
#
#

from django.contrib import admin

from apps.datasource_media_storages.models import DataSourceMediaStorageConnection
from apps.datasource_media_storages.utils import MEDIA_STORE_ADMIN_LIST_DISPLAY, MEDIA_STORE_ADMIN_LIST_FILTER, \
    MEDIA_STORE_ADMIN_SEARCH_FIELDS


@admin.register(DataSourceMediaStorageConnection)
class DataSourceMediaStorageConnectionAdmin(admin.ModelAdmin):
    list_display = MEDIA_STORE_ADMIN_LIST_DISPLAY
    list_filter = MEDIA_STORE_ADMIN_LIST_FILTER
    search_fields = MEDIA_STORE_ADMIN_SEARCH_FIELDS
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
