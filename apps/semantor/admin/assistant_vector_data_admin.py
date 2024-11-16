#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: assistant_vector_data_admin.py
#  Last Modified: 2024-11-09 18:19:45
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-09 18:19:46
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

from apps.semantor.models import AssistantVectorData
from apps.semantor.utils.constant_utils import ASSISTANT_VECTOR_DATA_ADMIN_LIST, ASSISTANT_VECTOR_DATA_ADMIN_SEARCH, \
    ASSISTANT_VECTOR_DATA_ADMIN_FILTER


@admin.register(AssistantVectorData)
class AssistantVectorDataAdmin(admin.ModelAdmin):
    list_display = ASSISTANT_VECTOR_DATA_ADMIN_LIST
    search_fields = ASSISTANT_VECTOR_DATA_ADMIN_SEARCH
    list_filter = ASSISTANT_VECTOR_DATA_ADMIN_FILTER
    ordering = ['-created_at']
