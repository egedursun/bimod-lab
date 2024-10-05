#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: assistant_memory_admin.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:34
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#

from django.contrib import admin

from apps.memories.models import AssistantMemory


@admin.register(AssistantMemory)
class AssistantMemoryAdmin(admin.ModelAdmin):
    list_display = ["user", "assistant", "memory_type", "created_at", "memory_text_content", "created_at"]
    list_filter = ["memory_type"]
    search_fields = ["user__username", "assistant__name"]
    date_hierarchy = "created_at"
    list_per_page = 20
    list_max_show_all = 100
    list_select_related = ["user", "assistant"]
    list_display_links = ["user", "assistant"]
    list_editable = ["memory_type"]
    readonly_fields = ["created_at"]
