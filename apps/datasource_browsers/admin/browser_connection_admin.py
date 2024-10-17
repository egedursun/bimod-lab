#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: browser_connection_admin.py
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

from apps.datasource_browsers.models import DataSourceBrowserConnection
from apps.datasource_browsers.utils import BROWSER_ADMIN_LIST, BROWSER_ADMIN_SEARCH, BROWSER_ADMIN_FILTER


@admin.register(DataSourceBrowserConnection)
class DataSourceBrowserConnectionAdmin(admin.ModelAdmin):
    list_display = BROWSER_ADMIN_LIST
    list_filter = BROWSER_ADMIN_FILTER
    search_fields = BROWSER_ADMIN_SEARCH
