#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: file_system_vector_admin.py
#  Last Modified: 2024-12-04 00:23:12
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-04 00:23:12
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

from apps.datasource_file_systems.models import (
    FileSystemDirectorySchemaChunkVectorData
)

from apps.datasource_file_systems.utils import (
    FILE_SYSTEM_DIRECTORY_SCHEMA_CHUNK_VECTOR_DATA_ADMIN_LIST,
    FILE_SYSTEM_DIRECTORY_SCHEMA_CHUNK_VECTOR_DATA_ADMIN_FILTER,
    FILE_SYSTEM_DIRECTORY_SCHEMA_CHUNK_VECTOR_DATA_ADMIN_SEARCH
)


@admin.register(FileSystemDirectorySchemaChunkVectorData)
class NoSQLSchemaChunkVectorDataAdmin(admin.ModelAdmin):
    list_display = FILE_SYSTEM_DIRECTORY_SCHEMA_CHUNK_VECTOR_DATA_ADMIN_LIST
    list_filter = FILE_SYSTEM_DIRECTORY_SCHEMA_CHUNK_VECTOR_DATA_ADMIN_FILTER
    search_fields = FILE_SYSTEM_DIRECTORY_SCHEMA_CHUNK_VECTOR_DATA_ADMIN_SEARCH

    ordering = ('created_at',)
