#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: blog_seo_meta_admin.py
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
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.contrib import admin

from apps.blog_app.models import BlogSEOMeta
from apps.blog_app.utils import BLOG_SEO_ADMIN_LIST, BLOG_SEO_ADMIN_FILTER, BLOG_SEO_ADMIN_SEARCH


@admin.register(BlogSEOMeta)
class BlogSEOMetaAdmin(admin.ModelAdmin):
    list_display = BLOG_SEO_ADMIN_LIST
    list_filter = BLOG_SEO_ADMIN_FILTER
    search_fields = BLOG_SEO_ADMIN_SEARCH
    ordering = ['post']
