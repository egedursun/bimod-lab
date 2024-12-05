#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: export_orchestration_admin.py
#  Last Modified: 2024-10-05 01:39:48
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

from django.contrib import admin

from apps.export_voidforger.models import ExportVoidForgerAPI

from apps.export_voidforger.utils import (
    EXPORT_VOIDFORGER_ADMIN_LIST,
    EXPORT_VOIDFORGER_ADMIN_FILTER,
    EXPORT_VOIDFORGER_ADMIN_SEARCH
)


@admin.register(ExportVoidForgerAPI)
class ExportVoidForgerAssistantAPIAdmin(admin.ModelAdmin):
    list_display = EXPORT_VOIDFORGER_ADMIN_LIST
    list_filter = EXPORT_VOIDFORGER_ADMIN_FILTER
    search_fields = EXPORT_VOIDFORGER_ADMIN_SEARCH

    date_hierarchy = "created_at"
    ordering = ["-created_at"]
