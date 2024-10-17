#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.contrib import admin

from apps.memories.models import AssistantMemory
from apps.memories.utils import MEMORIES_ADMIN_LIST, MEMORIES_ADMIN_FILTER, MEMORIES_ADMIN_SEARCH


@admin.register(AssistantMemory)
class AssistantMemoryAdmin(admin.ModelAdmin):
    list_display = MEMORIES_ADMIN_LIST
    list_filter = MEMORIES_ADMIN_FILTER
    search_fields = MEMORIES_ADMIN_SEARCH
    date_hierarchy = "created_at"
