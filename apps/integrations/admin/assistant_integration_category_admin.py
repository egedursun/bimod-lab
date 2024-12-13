#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: assistant_integration_category_admin.py
#  Last Modified: 2024-11-05 19:24:01
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-05 19:24:01
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

from apps.integrations.models import (
    AssistantIntegrationCategory
)

from apps.integrations.utils import (
    ASSISTANT_INTEGRATION_CATEGORY_ADMIN_LIST,
    ASSISTANT_INTEGRATION_CATEGORY_ADMIN_SEARCH,
    ASSISTANT_INTEGRATION_CATEGORY_ADMIN_FILTER
)


@admin.register(AssistantIntegrationCategory)
class AssistantIntegrationCategoryAdmin(admin.ModelAdmin):
    list_display = ASSISTANT_INTEGRATION_CATEGORY_ADMIN_LIST
    search_fields = ASSISTANT_INTEGRATION_CATEGORY_ADMIN_SEARCH
    list_filter = ASSISTANT_INTEGRATION_CATEGORY_ADMIN_FILTER

    ordering = ['-created_at']
