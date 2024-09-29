#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: browsing_log_admin.py
#  Last Modified: 2024-09-26 20:04:16
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:31:41
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import admin

from apps.datasource_browsers.models import DataSourceBrowserBrowsingLog


@admin.register(DataSourceBrowserBrowsingLog)
class DataSourceBrowserBrowsingLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'connection', 'action', 'created_at']
    list_filter = ['connection', 'action', 'created_at']
    search_fields = ['connection', 'action', 'html_content', 'log_content', 'created_at']
    list_per_page = 20
    list_max_show_all = 100
