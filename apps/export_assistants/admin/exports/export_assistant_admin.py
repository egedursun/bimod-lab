#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: export_assistant_admin.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:44
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

from apps.export_assistants.models import ExportAssistantAPI

from apps.export_assistants.utils import (
    EXPORT_ASSISTANT_API_ADMIN_LIST,
    EXPORT_ASSISTANT_API_ADMIN_FILTER,
    EXPORT_ASSISTANT_API_ADMIN_SEARCH
)


@admin.register(ExportAssistantAPI)
class ExportAssistantAPIAdmin(admin.ModelAdmin):
    list_display = EXPORT_ASSISTANT_API_ADMIN_LIST
    list_filter = EXPORT_ASSISTANT_API_ADMIN_FILTER
    search_fields = EXPORT_ASSISTANT_API_ADMIN_SEARCH
    date_hierarchy = "created_at"
    ordering = ["-created_at"]
