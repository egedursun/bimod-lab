#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: code_repository_processing_log_admin.py
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

from apps.datasource_codebase.models import RepositoryProcessingLog

from apps.datasource_codebase.utils import (
    CODE_REPOSITORY_LOG_ADMIN_LIST,
    CODE_REPOSITORY_LOG_ADMIN_FILTER,
    CODE_REPOSITORY_LOG_ADMIN_SEARCH
)


@admin.register(RepositoryProcessingLog)
class RepositoryProcessingLogAdmin(admin.ModelAdmin):
    list_display = CODE_REPOSITORY_LOG_ADMIN_LIST
    list_filter = CODE_REPOSITORY_LOG_ADMIN_FILTER
    search_fields = CODE_REPOSITORY_LOG_ADMIN_SEARCH

    readonly_fields = ['created_at']

    list_per_page = 20
    list_max_show_all = 100
