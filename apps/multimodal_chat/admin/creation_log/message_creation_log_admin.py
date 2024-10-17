#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: message_creation_log_admin.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:43
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

from apps.multimodal_chat.models import ChatMessageCreationLog
from apps.multimodal_chat.utils import CHAT_MESSAGE_CREATION_LOG_ADMIN_LIST, CHAT_MESSAGE_CREATION_LOG_ADMIN_FILTER, \
    CHAT_MESSAGE_CREATION_LOG_ADMIN_SEARCH


@admin.register(ChatMessageCreationLog)
class ChatMessageCreationLogAdmin(admin.ModelAdmin):
    list_display = CHAT_MESSAGE_CREATION_LOG_ADMIN_LIST
    list_filter = CHAT_MESSAGE_CREATION_LOG_ADMIN_FILTER
    search_fields = CHAT_MESSAGE_CREATION_LOG_ADMIN_SEARCH
