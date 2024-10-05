#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: llm_core_admin.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:32
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: llm_core_admin.py
#  Last Modified: 2024-09-27 17:27:16
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:55:52
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import admin

from apps.llm_core.models import LLMCore


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "address", "industry", "is_active", "created_at", "updated_at")
    list_filter = ("is_active", "industry", "created_at", "updated_at")
    search_fields = ("name", "email", "phone", "address", "industry")
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    list_per_page = 20
    list_max_show_all = 100
    list_editable = ["is_active"]
    list_display_links = ["name"]
    list_select_related = False
    list_display_links_details = False


@admin.register(LLMCore)
class LLMCoreAdmin(admin.ModelAdmin):
    list_display = ("nickname", "provider", "model_name", "temperature", "maximum_tokens", "stop_sequences", "top_p",
                    "frequency_penalty", "presence_penalty", "created_at", "updated_at")
    list_filter = ("provider", "model_name", "temperature", "maximum_tokens", "top_p", "frequency_penalty",
                   "presence_penalty", "created_at", "updated_at")
    search_fields = ("nickname", "provider", "model_name", "temperature", "maximum_tokens", "stop_sequences", "top_p",
                     "frequency_penalty", "presence_penalty")
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    list_per_page = 20
    list_max_show_all = 100
    list_editable = ["provider", "model_name", "temperature", "maximum_tokens", "stop_sequences", "top_p",
                     "frequency_penalty", "presence_penalty"]
    list_display_links = ["nickname"]
    list_select_related = False
    list_display_links_details = False
