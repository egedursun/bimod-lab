#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

#
from django.contrib import admin

from apps.multimodal_chat.models import ChatMessageCreationLog


@admin.register(ChatMessageCreationLog)
class ChatMessageCreationLogAdmin(admin.ModelAdmin):
    list_display = ["organization", 'created_at']
    list_filter = ['created_at']
    search_fields = ['created_at']
