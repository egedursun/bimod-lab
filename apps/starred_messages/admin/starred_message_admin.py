#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: starred_message_admin.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:42
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
#  File: starred_message_admin.py
#  Last Modified: 2024-09-27 16:38:28
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:08:23
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import admin

from apps.starred_messages.models import StarredMessage


@admin.register(StarredMessage)
class StarredMessageAdmin(admin.ModelAdmin):
    list_display = ["user", "organization", "assistant", "chat", "chat_message", "starred_at", "message_text"]
    list_filter = ["user", "organization", "assistant", "chat", "chat_message", "starred_at", "message_text"]
    search_fields = ["user", "organization", "assistant", "chat", "chat_message", "starred_at", "message_text"]
    list_per_page = 20
    ordering = ["-starred_at"]
    readonly_fields = ["starred_at"]
    fieldsets = [
        (
        None, {"fields": ["user", "organization", "assistant", "chat", "chat_message", "starred_at", "message_text"]}),
    ]
    add_fieldsets = [
        (
        None, {"fields": ["user", "organization", "assistant", "chat", "chat_message", "starred_at", "message_text"]}),
    ]
