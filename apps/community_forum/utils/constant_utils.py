#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
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
#
#
#

CONST_SECONDS = 1
CONST_MINUTES = 60 * CONST_SECONDS
CONST_HOURS = 60 * CONST_MINUTES

FORUM_CATEGORY_ADMIN_LIST = ("name", "slug", "created_at", "updated_at",)
FORUM_CATEGORY_ADMIN_SEARCH = ("name", "description", "slug",)
FORUM_CATEGORY_ADMIN_FILTER = ("created_at", "updated_at",)

FORUM_COMMENT_ADMIN_LIST = ("post", "content", "created_by", "created_at", "updated_at")
FORUM_COMMENT_ADMIN_SEARCH = ("post__content", "content", "created_by__username",)
FORUM_COMMENT_ADMIN_FILTER = ("created_at", "updated_at",)

FORUM_LIKE_ADMIN_LIST = ("user", "created_at")
FORUM_LIKE_ADMIN_SEARCH = ("comment",)
FORUM_LIKE_ADMIN_FILTER = ("created_at",)

FORUM_POST_ADMIN_LIST = ("thread", "content", "created_by", "created_at", "updated_at", "is_verified",)
FORUM_POST_ADMIN_SEARCH = ("thread__title", "content", "created_by__username",)
FORUM_POST_ADMIN_FILTER = ("created_at", "updated_at", "is_verified",)

FORUM_THREAD_ADMIN_LIST = ("title", "category", "created_by", "created_at", "updated_at", "is_closed",)
FORUM_THREAD_ADMIN_SEARCH = ("title", "category__name", "created_by__username",)
FORUM_THREAD_ADMIN_FILTER = ("created_at", "updated_at", "is_closed",)
