#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: browsing_log_admin.py
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

from apps.datasource_browsers.models import DataSourceBrowserBrowsingLog


@admin.register(DataSourceBrowserBrowsingLog)
class DataSourceBrowserBrowsingLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'connection', 'action', 'created_at']
    list_filter = ['connection', 'action', 'created_at']
    search_fields = ['connection', 'action', 'html_content', 'log_content', 'created_at']
    list_per_page = 20
    list_max_show_all = 100
