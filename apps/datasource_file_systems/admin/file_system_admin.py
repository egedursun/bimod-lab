#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: file_system_admin.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:46
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

from apps.datasource_file_systems.models import DataSourceFileSystem

from apps.datasource_file_systems.utils import (
    FILE_SYSTEM_ADMIN_LIST,
    FILE_SYSTEM_ADMIN_FILTER,
    FILE_SYSTEM_ADMIN_SEARCH
)


@admin.register(DataSourceFileSystem)
class DataSourceFileSystemAdmin(admin.ModelAdmin):
    list_display = FILE_SYSTEM_ADMIN_LIST
    list_filter = FILE_SYSTEM_ADMIN_FILTER
    search_fields = FILE_SYSTEM_ADMIN_SEARCH

    ordering = ('-created_at',)

    readonly_fields = (
        'created_at',
        'updated_at'
    )

    date_hierarchy = 'created_at'
    save_on_top = True
