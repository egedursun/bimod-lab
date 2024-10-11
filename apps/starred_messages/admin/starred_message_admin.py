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


from django.contrib import admin

from apps.starred_messages.models import StarredMessage
from apps.starred_messages.utils import STARRED_MESSAGE_ADMIN_LIST, STARRED_MESSAGE_ADMIN_FILTER, \
    STARRED_MESSAGE_ADMIN_SEARCH


@admin.register(StarredMessage)
class StarredMessageAdmin(admin.ModelAdmin):
    list_display = STARRED_MESSAGE_ADMIN_LIST
    list_filter = STARRED_MESSAGE_ADMIN_FILTER
    search_fields = STARRED_MESSAGE_ADMIN_SEARCH
    ordering = ["-starred_at"]
