#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: chat_creation_log_admin.py
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

from apps.multimodal_chat.models import ChatCreationLog


@admin.register(ChatCreationLog)
class ChatCreationLogAdmin(admin.ModelAdmin):
    list_display = ["organization", 'created_at']
    list_filter = ['created_at']
    search_fields = ['created_at']
