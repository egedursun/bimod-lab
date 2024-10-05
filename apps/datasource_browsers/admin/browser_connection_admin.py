#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: browser_connection_admin.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:43
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: browser_connection_admin.py
#  Last Modified: 2024-09-26 20:04:16
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:31:37
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import admin

from apps.datasource_browsers.models import DataSourceBrowserConnection


@admin.register(DataSourceBrowserConnection)
class DataSourceBrowserConnectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'assistant', 'browser_type', 'name', 'description', 'data_selectivity',
                    'whitelisted_extensions', 'blacklisted_extensions', 'created_at', 'updated_at']
    list_filter = ['assistant', 'browser_type', 'data_selectivity']
    search_fields = ['assistant', 'browser_type', 'name', 'description', 'data_selectivity', 'whitelisted_extensions',
                     'blacklisted_extensions', 'created_at', 'updated_at']
    list_per_page = 20
    list_max_show_all = 100
