#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: forum_post_admin.py
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.contrib import admin

from apps.community_forum.models import ForumPost
from apps.community_forum.utils import FORUM_POST_ADMIN_LIST, FORUM_POST_ADMIN_SEARCH, FORUM_POST_ADMIN_FILTER


@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = FORUM_POST_ADMIN_LIST
    search_fields = FORUM_POST_ADMIN_SEARCH
    list_filter = FORUM_POST_ADMIN_FILTER
    ordering = ("-created_at",)
