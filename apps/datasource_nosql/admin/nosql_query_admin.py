#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: nosql_query_admin.py
#  Last Modified: 2024-10-12 13:08:45
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-12 13:08:46
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

from apps.datasource_nosql.models import CustomNoSQLQuery

from apps.datasource_nosql.utils import (
    NOSQL_QUERY_ADMIN_LIST,
    NOSQL_QUERY_ADMIN_FILTER,
    NOSQL_QUERY_ADMIN_SEARCH
)


@admin.register(CustomNoSQLQuery)
class CustomNoSQLQueryAdmin(admin.ModelAdmin):
    list_display = NOSQL_QUERY_ADMIN_LIST
    list_filter = NOSQL_QUERY_ADMIN_FILTER
    search_fields = NOSQL_QUERY_ADMIN_SEARCH

    ordering = ('-created_at',)
