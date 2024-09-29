#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: forum_comment_admin.py
#  Last Modified: 2024-09-26 19:10:04
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:20:55
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import admin

from apps.community_forum.models import ForumComment


@admin.register(ForumComment)
class ForumCommentAdmin(admin.ModelAdmin):
    list_display = (
        "post", "content", "created_by", "created_at", "updated_at"
    )
    search_fields = ("post__content", "content", "created_by__username",)
    list_filter = ("created_at", "updated_at",)
    ordering = ("-created_at",)
