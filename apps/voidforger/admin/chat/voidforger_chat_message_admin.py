#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: voidforger_chat_message_admin.py
#  Last Modified: 2024-11-15 17:32:18
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-15 17:32:19
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

from apps.voidforger.models import (
    MultimodalVoidForgerChatMessage
)

from apps.voidforger.utils import (
    VOIDFORGER_CHAT_MESSAGE_ADMIN_LIST,
    VOIDFORGER_CHAT_MESSAGE_ADMIN_FILTER,
    VOIDFORGER_CHAT_MESSAGE_ADMIN_SEARCH
)


@admin.register(MultimodalVoidForgerChatMessage)
class MultimodalVoidForgerChatMessageAdmin(admin.ModelAdmin):
    list_display = VOIDFORGER_CHAT_MESSAGE_ADMIN_LIST
    list_filter = VOIDFORGER_CHAT_MESSAGE_ADMIN_FILTER
    search_fields = VOIDFORGER_CHAT_MESSAGE_ADMIN_SEARCH

    ordering = ['-sent_at']
