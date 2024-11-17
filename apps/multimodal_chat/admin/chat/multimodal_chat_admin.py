#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: multimodal_chat_admin.py
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

from apps.multimodal_chat.models import MultimodalChat

from apps.multimodal_chat.utils import MULTIMODAL_CHAT_ADMIN_LIST, MULTIMODAL_CHAT_ADMIN_FILTER, \
    MULTIMODAL_CHAT_ADMIN_SEARCH


@admin.register(MultimodalChat)
class MultimodalChatAdmin(admin.ModelAdmin):
    list_display = MULTIMODAL_CHAT_ADMIN_LIST
    list_filter = MULTIMODAL_CHAT_ADMIN_FILTER
    search_fields = MULTIMODAL_CHAT_ADMIN_SEARCH
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20
    list_max_show_all = 100
    list_editable = []
    list_display_links = ["organization"]
    list_select_related = False
    list_display_links_details = False

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
