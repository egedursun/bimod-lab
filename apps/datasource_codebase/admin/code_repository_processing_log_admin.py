#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.contrib import admin

from apps.datasource_codebase.models import RepositoryProcessingLog


@admin.register(RepositoryProcessingLog)
class RepositoryProcessingLogAdmin(admin.ModelAdmin):
    list_display = ['repository_full_uri', 'log_message', 'created_at']
    list_filter = ['repository_full_uri', 'log_message', 'created_at']
    search_fields = ['repository_full_uri', 'log_message']
    readonly_fields = ['created_at']

    list_per_page = 20
    list_max_show_all = 100
