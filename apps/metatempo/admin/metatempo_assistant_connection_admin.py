#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: metatempo_assistant_connection_admin.py
#  Last Modified: 2024-11-13 03:17:17
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-13 03:17:17
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

from apps.metatempo.models import (
    MetaTempoAssistantConnection
)

from apps.metatempo.utils import (
    METATEMPO_ASSISTANT_CONNECTION_ADMIN_LIST,
    METATEMPO_ASSISTANT_CONNECTION_ADMIN_FILTER,
    METATEMPO_ASSISTANT_CONNECTION_ADMIN_SEARCH
)


@admin.register(MetaTempoAssistantConnection)
class MetaTempoAssistantConnectionAdmin(admin.ModelAdmin):
    list_display = METATEMPO_ASSISTANT_CONNECTION_ADMIN_LIST
    list_filter = METATEMPO_ASSISTANT_CONNECTION_ADMIN_FILTER
    search_fields = METATEMPO_ASSISTANT_CONNECTION_ADMIN_SEARCH

    ordering = ["-created_at"]
