#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: blog_tag_admin.py
#  Last Modified: 2024-10-05 12:51:58
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:34
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

from apps.blog_app.models import BlogTag
from apps.blog_app.utils import BLOG_TAG_ADMIN_LIST, BLOG_TAG_ADMIN_FILTER, BLOG_TAG_ADMIN_SEARCH


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = BLOG_TAG_ADMIN_LIST
    list_filter = BLOG_TAG_ADMIN_FILTER
    search_fields = BLOG_TAG_ADMIN_SEARCH
    ordering = ['name']
