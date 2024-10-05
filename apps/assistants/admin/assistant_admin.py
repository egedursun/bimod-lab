#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: assistant_admin.py
#  Last Modified: 2024-10-05 12:51:58
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:37
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


from django.contrib import admin

from apps.assistants.models import Assistant


@admin.register(Assistant)
class AssistantAdmin(admin.ModelAdmin):
    list_display = (
        "organization", "response_language", "llm_model", "name", "instructions", "audience", "tone",
        "time_awareness", "place_awareness", "tool_max_attempts_per_instance", "tool_max_chains",
        "document_base_directory", "max_retry_count", "created_by_user", "last_updated_by_user", "created_at",
        "updated_at")
    list_filter = (
        "organization", "response_language", "llm_model", "name", "instructions", "audience", "tone",
        "document_base_directory", "time_awareness", "place_awareness", "tool_max_attempts_per_instance",
        "tool_max_chains", "max_retry_count", "created_by_user", "last_updated_by_user", "created_at", "updated_at")
    search_fields = (
        "organization", "response_language", "llm_model", "name", "instructions", "audience", "tone",
        "document_base_directory", "time_awareness", "place_awareness", "tool_max_attempts_per_instance",
        "tool_max_chains", "max_retry_count", "created_by_user", "last_updated_by_user", "created_at", "updated_at")
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    list_per_page = 20
    list_max_show_all = 100
    list_editable = []
    list_display_links = ["organization"]
    list_select_related = False
    list_display_links_details = False
