#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: media_item_admin.py
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.contrib import admin

from apps.datasource_media_storages.models import DataSourceMediaStorageItem


@admin.register(DataSourceMediaStorageItem)
class DataSourceMediaStorageItemAdmin(admin.ModelAdmin):
    list_display = ['storage_base', 'media_file_name', 'media_file_size', 'media_file_type', 'full_file_path',
                    'created_at', 'updated_at']
    list_filter = ['storage_base', 'media_file_type', 'media_file_type']
    search_fields = ['storage_base', 'media_file_name', 'full_file_path']

    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']

    list_per_page = 20
    list_max_show_all = 100
