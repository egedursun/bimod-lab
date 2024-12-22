#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: knowledge_base_integration_admin.py
#  Last Modified: 2024-12-21 19:09:42
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-21 19:09:43
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

from apps.knowledge_base_store.models import (
    KnowledgeBaseIntegration
)

from apps.knowledge_base_store.utils import (
    KNOWLEDGE_BASE_INTEGRATION_ADMIN_LIST,
    KNOWLEDGE_BASE_INTEGRATION_ADMIN_FILTER,
    KNOWLEDGE_BASE_INTEGRATION_ADMIN_SEARCH
)


@admin.register(KnowledgeBaseIntegration)
class KnowledgeBaseIntegrationAdmin(admin.ModelAdmin):
    list_display = KNOWLEDGE_BASE_INTEGRATION_ADMIN_LIST
    list_filter = KNOWLEDGE_BASE_INTEGRATION_ADMIN_FILTER
    search_fields = KNOWLEDGE_BASE_INTEGRATION_ADMIN_SEARCH

    ordering = ["-created_at"]
