#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: starred_message_admin.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:44
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

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
