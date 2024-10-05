#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.contrib import admin

from apps.export_orchestrations.models import ExportOrchestrationAPI


@admin.register(ExportOrchestrationAPI)
class ExportOrchestrationAssistantAPIAdmin(admin.ModelAdmin):
    list_display = (
        "orchestrator", "is_public", "request_limit_per_hour", "custom_api_key", "created_by_user",
        "is_online", "created_at", "updated_at")
    list_filter = (
        "orchestrator", "is_public", "request_limit_per_hour", "custom_api_key", "created_by_user",
        "is_online", "created_at", "updated_at")
    search_fields = (
        "orchestrator", "is_public", "request_limit_per_hour", "custom_api_key", "created_by_user",
        "is_online", "created_at", "updated_at")
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    list_per_page = 20
    list_max_show_all = 100
    list_editable = []
    list_display_links = ["orchestrator"]
    list_select_related = False
    list_display_links_details = False
