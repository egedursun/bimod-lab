#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: sql_query_admin.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:40
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

from apps.datasource_sql.models import CustomSQLQuery
from apps.datasource_sql.utils import SQL_QUERY_ADMIN_LIST, SQL_QUERY_ADMIN_FILTER, SQL_QUERY_ADMIN_SEARCH


@admin.register(CustomSQLQuery)
class CustomSQLQueryAdmin(admin.ModelAdmin):
    list_display = SQL_QUERY_ADMIN_LIST
    list_filter = SQL_QUERY_ADMIN_FILTER
    search_fields = SQL_QUERY_ADMIN_SEARCH
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
