#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: multimodal_lean_chat_admin.py
#  Last Modified: 2024-09-28 20:38:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:05:10
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

#
from django.contrib import admin

from apps.multimodal_chat.models import MultimodalLeanChat


@admin.register(MultimodalLeanChat)
class MultimodalLeanChatAdmin(admin.ModelAdmin):
    list_display = ['organization', 'lean_assistant', 'user', 'chat_name', 'created_by_user', 'created_at',
                    'updated_at']
    list_filter = ['organization', 'lean_assistant', 'user', 'created_by_user', 'created_at', 'updated_at']
    search_fields = ['organization', 'lean_assistant', 'user', 'chat_name', 'created_by_user', 'created_at',
                     'updated_at']
    readonly_fields = ['created_at', 'updated_at']

    list_per_page = 20
    list_max_show_all = 100
    list_editable = []
    list_display_links = ["organization"]
    list_select_related = False
    list_display_links_details = False
