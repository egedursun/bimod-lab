#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: message_template_admin.py
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

from apps.message_templates.models import MessageTemplate


@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = ["user", "organization", "template_text", "created_at", "updated_at"]
    search_fields = ["user", "organization", "template_text"]
    list_filter = ["user", "organization", "created_at", "updated_at"]
    list_per_page = 20
    list_max_show_all = 200
    list_editable = ["template_text"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        (None, {"fields": ("user", "organization", "template_text")}),
        ("Date Information", {"fields": ("created_at", "updated_at")})
    )
    actions = ["delete_selected"]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]
