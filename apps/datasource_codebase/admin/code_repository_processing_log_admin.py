#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: code_repository_processing_log_admin.py
#  Last Modified: 2024-09-26 20:30:21
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:36:39
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

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
