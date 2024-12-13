#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: meta_kanban_assistant_connections_admin.py
#  Last Modified: 2024-11-13 02:47:31
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-13 02:47:31
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

from apps.metakanban.models import (
    MetaKanbanAssistantConnection
)

from apps.metakanban.utils import (
    METAKANBAN_ASSISTANT_CONNECTION_ADMIN_LIST,
    METAKANBAN_ASSISTANT_CONNECTION_ADMIN_SEARCH,
    METAKANBAN_ASSISTANT_CONNECTION_ADMIN_FILTER
)


@admin.register(MetaKanbanAssistantConnection)
class MetaKanbanAssistantConnectionAdmin(admin.ModelAdmin):
    list_display = METAKANBAN_ASSISTANT_CONNECTION_ADMIN_LIST
    search_fields = METAKANBAN_ASSISTANT_CONNECTION_ADMIN_SEARCH
    list_filter = METAKANBAN_ASSISTANT_CONNECTION_ADMIN_FILTER

    ordering = ["-created_at"]
