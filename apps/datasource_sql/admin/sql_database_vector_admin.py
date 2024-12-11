#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: sql_database_vector_admin.py
#  Last Modified: 2024-12-03 22:29:35
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-03 22:29:36
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

from apps.datasource_sql.models import (
    SQLSchemaChunkVectorData
)

from apps.datasource_sql.utils import (
    SQL_SCHEMA_CHUNK_VECTOR_DATA_ADMIN_LIST,
    SQL_SCHEMA_CHUNK_VECTOR_DATA_ADMIN_SEARCH,
    SQL_SCHEMA_CHUNK_VECTOR_DATA_ADMIN_FILTER
)


@admin.register(SQLSchemaChunkVectorData)
class SQLSchemaChunkVectorDataAdmin(admin.ModelAdmin):
    list_display = SQL_SCHEMA_CHUNK_VECTOR_DATA_ADMIN_LIST
    search_fields = SQL_SCHEMA_CHUNK_VECTOR_DATA_ADMIN_SEARCH
    list_filter = SQL_SCHEMA_CHUNK_VECTOR_DATA_ADMIN_FILTER

    ordering = ('-created_at',)
