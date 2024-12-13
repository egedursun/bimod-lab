#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: llm_core_admin.py
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

from apps.llm_core.models import LLMCore

from apps.llm_core.utils import (
    LLM_CORE_ADMIN_LIST,
    LLM_CORE_ADMIN_FILTER,
    LLM_CORE_ADMIN_SEARCH
)


@admin.register(LLMCore)
class LLMCoreAdmin(admin.ModelAdmin):
    list_display = LLM_CORE_ADMIN_LIST
    list_filter = LLM_CORE_ADMIN_FILTER
    search_fields = LLM_CORE_ADMIN_SEARCH

    date_hierarchy = "created_at"
    ordering = ["-created_at"]
