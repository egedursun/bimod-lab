#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: formica_google_apps_connection_admin.py
#  Last Modified: 2024-11-02 12:47:00
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-02 12:47:01
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

from apps.formica.models import FormicaGoogleAppsConnection

from apps.formica.utils import (
    FORMICA_GOOGLE_APPS_CONNECTION_ADMIN_LIST,
    FORMICA_GOOGLE_APPS_CONNECTION_ADMIN_FILTER,
    FORMICA_GOOGLE_APPS_CONNECTION_ADMIN_SEARCH
)


@admin.register(FormicaGoogleAppsConnection)
class DraftingGoogleAppsConnectionAdmin(admin.ModelAdmin):
    list_display = FORMICA_GOOGLE_APPS_CONNECTION_ADMIN_LIST
    list_filter = FORMICA_GOOGLE_APPS_CONNECTION_ADMIN_FILTER
    search_fields = FORMICA_GOOGLE_APPS_CONNECTION_ADMIN_SEARCH

    ordering = ('-created_at', '-updated_at')
