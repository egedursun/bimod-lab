#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: forum_thread_admin.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:41
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

from apps.community_forum.models import ForumThread

from apps.community_forum.utils import (
    FORUM_THREAD_ADMIN_LIST,
    FORUM_THREAD_ADMIN_SEARCH,
    FORUM_THREAD_ADMIN_FILTER
)


@admin.register(ForumThread)
class ForumThreadAdmin(admin.ModelAdmin):
    list_display = FORUM_THREAD_ADMIN_LIST
    search_fields = FORUM_THREAD_ADMIN_SEARCH
    list_filter = FORUM_THREAD_ADMIN_FILTER

    ordering = ("-created_at",)
