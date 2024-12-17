#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: leanmod_assistant_vector_data_admin.py
#  Last Modified: 2024-11-16 00:26:37
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-16 00:26:38
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

from apps.semantor.models import (
    LeanModVectorData
)

from apps.semantor.utils.constant_utils import (
    LEANMOD_ASSISTANT_VECTOR_DATA_ADMIN_LIST,
    LEANMOD_ASSISTANT_VECTOR_DATA_ADMIN_SEARCH,
    LEANMOD_ASSISTANT_VECTOR_DATA_ADMIN_FILTER
)


@admin.register(LeanModVectorData)
class AssistantVectorDataAdmin(admin.ModelAdmin):
    list_display = LEANMOD_ASSISTANT_VECTOR_DATA_ADMIN_LIST
    search_fields = LEANMOD_ASSISTANT_VECTOR_DATA_ADMIN_SEARCH
    list_filter = LEANMOD_ASSISTANT_VECTOR_DATA_ADMIN_FILTER

    ordering = ['-created_at']
