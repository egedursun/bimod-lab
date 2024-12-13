#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: leanmod_context_history_vector_admin.py
#  Last Modified: 2024-11-17 20:47:35
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-17 20:47:35
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from apps.leanmod.models import (
    LeanModOldChatMessagesVectorData
)

from django.contrib import admin

from apps.leanmod.utils import (
    LEANMOD_OLD_CHAT_MESSAGES_VECTOR_DATA_ADMIN_LIST,
    LEANMOD_OLD_CHAT_MESSAGES_VECTOR_DATA_ADMIN_FILTER,
    LEANMOD_OLD_CHAT_MESSAGES_VECTOR_DATA_ADMIN_SEARCH
)


@admin.register(LeanModOldChatMessagesVectorData)
class LeanModOldChatMessagesVectorDataAdmin(admin.ModelAdmin):
    list_display = LEANMOD_OLD_CHAT_MESSAGES_VECTOR_DATA_ADMIN_LIST
    list_filter = LEANMOD_OLD_CHAT_MESSAGES_VECTOR_DATA_ADMIN_FILTER
    search_fields = LEANMOD_OLD_CHAT_MESSAGES_VECTOR_DATA_ADMIN_SEARCH

    ordering = ['-created_at']
