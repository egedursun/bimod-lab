#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: media_storage_admin.py
#  Last Modified: 2024-09-27 12:19:22
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:46:07
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import admin

from apps.datasource_media_storages.models import DataSourceMediaStorageConnection


@admin.register(DataSourceMediaStorageConnection)
class DataSourceMediaStorageConnectionAdmin(admin.ModelAdmin):
    list_display = ['assistant', 'name', 'media_category', 'directory_full_path', 'directory_schema', 'created_at',
                    'updated_at']
    list_filter = ['assistant', 'media_category']
    search_fields = ['assistant', 'name', 'directory_full_path']

    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']

    list_per_page = 20
    list_max_show_all = 100
