#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: sheetos_google_apps_connection_admin.py
#  Last Modified: 2024-10-31 18:34:58
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-31 18:34:59
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

from apps.sheetos.models import (
    SheetosGoogleAppsConnection
)

from apps.sheetos.utils import (
    SHEETOS_GOOGLE_APPS_CONNECTION_ADMIN_LIST,
    SHEETOS_GOOGLE_APPS_CONNECTION_ADMIN_FILTER,
    SHEETOS_GOOGLE_APPS_CONNECTION_ADMIN_SEARCH
)


@admin.register(SheetosGoogleAppsConnection)
class SheetosGoogleAppsConnectionAdmin(admin.ModelAdmin):
    list_display = SHEETOS_GOOGLE_APPS_CONNECTION_ADMIN_LIST
    list_filter = SHEETOS_GOOGLE_APPS_CONNECTION_ADMIN_FILTER
    search_fields = SHEETOS_GOOGLE_APPS_CONNECTION_ADMIN_SEARCH

    ordering = ('-created_at', '-updated_at')
