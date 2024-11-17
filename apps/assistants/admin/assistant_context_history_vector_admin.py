#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: assistant_context_history_vector_admin.py
#  Last Modified: 2024-11-17 20:11:27
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-17 20:11:34
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

from apps.assistants.models import AssistantOldChatMessagesVectorData
from apps.assistants.utils import ASSISTANT_OLD_CHAT_MESSAGES_VECTOR_DATA_ADMIN_SEARCH, \
    ASSISTANT_OLD_CHAT_MESSAGES_VECTOR_DATA_ADMIN_FILTER, ASSISTANT_OLD_CHAT_MESSAGES_VECTOR_DATA_ADMIN_LIST


@admin.register(AssistantOldChatMessagesVectorData)
class VoidForgerOldChatMessagesVectorDataAdmin(admin.ModelAdmin):
    list_display = ASSISTANT_OLD_CHAT_MESSAGES_VECTOR_DATA_ADMIN_LIST
    list_filter = ASSISTANT_OLD_CHAT_MESSAGES_VECTOR_DATA_ADMIN_FILTER
    search_fields = ASSISTANT_OLD_CHAT_MESSAGES_VECTOR_DATA_ADMIN_SEARCH
    ordering = ['-created_at']
