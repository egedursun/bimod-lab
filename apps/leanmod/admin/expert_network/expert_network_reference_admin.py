#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: expert_network_reference_admin.py
#  Last Modified: 2024-09-27 18:09:46
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:54:57
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import admin

from apps.leanmod.models import ExpertNetworkAssistantReference


@admin.register(ExpertNetworkAssistantReference)
class ExpertNetworkAssistantReferenceAdmin(admin.ModelAdmin):
    list_display = (
        "network", "assistant", "context_instructions", "created_by_user", "last_updated_by_user", "created_at",
        "updated_at")
    list_filter = (
        "network", "assistant", "context_instructions", "created_by_user", "last_updated_by_user", "created_at",
        "updated_at")
    search_fields = (
        "network", "assistant", "context_instructions", "created_by_user", "last_updated_by_user", "created_at",
        "updated_at")
    date_hierarchy = "created_at"
    ordering = ["-created_at"]
