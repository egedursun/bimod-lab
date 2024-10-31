#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: drafting_google_apps_connection_models.py
#  Last Modified: 2024-10-31 03:20:52
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-31 03:20:53
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

from apps.drafting.models import DraftingGoogleAppsConnection
from apps.drafting.utils import DRAFTING_GOOGLE_APPS_CONNECTION_ADMIN_LIST, \
    DRAFTING_GOOGLE_APPS_CONNECTION_ADMIN_FILTER, DRAFTING_GOOGLE_APPS_CONNECTION_ADMIN_SEARCH


@admin.register(DraftingGoogleAppsConnection)
class DraftingGoogleAppsConnectionAdmin(admin.ModelAdmin):
    list_display = DRAFTING_GOOGLE_APPS_CONNECTION_ADMIN_LIST
    list_filter = DRAFTING_GOOGLE_APPS_CONNECTION_ADMIN_FILTER
    search_fields = DRAFTING_GOOGLE_APPS_CONNECTION_ADMIN_SEARCH
    ordering = ('-created_at', '-updated_at')
