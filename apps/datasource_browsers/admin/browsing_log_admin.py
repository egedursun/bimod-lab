#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#
#
#
#

from django.contrib import admin

from apps.datasource_browsers.models import DataSourceBrowserBrowsingLog
from apps.datasource_browsers.utils import BROWSING_LOG_ADMIN_LIST, BROWSING_LOG_ADMIN_SEARCH, \
    BROWSING_LOG_ADMIN_FILTER


@admin.register(DataSourceBrowserBrowsingLog)
class DataSourceBrowserBrowsingLogAdmin(admin.ModelAdmin):
    list_display = BROWSING_LOG_ADMIN_LIST
    list_filter = BROWSING_LOG_ADMIN_FILTER
    search_fields = BROWSING_LOG_ADMIN_SEARCH
    list_per_page = 20
    list_max_show_all = 100
