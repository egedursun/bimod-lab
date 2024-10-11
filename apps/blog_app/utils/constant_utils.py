#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: constant_utils.py
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

STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
)


BLOG_POST_ADMIN_LIST = ['title', 'status', 'published_at', 'created_at', 'updated_at']
BLOG_POST_ADMIN_FILTER = ['status', 'published_at', 'created_at', 'updated_at']
BLOG_POST_ADMIN_SEARCH = ['title', 'content']

BLOG_SEO_ADMIN_LIST = ['post', 'meta_title', 'meta_description', 'meta_keywords']
BLOG_SEO_ADMIN_FILTER = ['meta_title', 'meta_description', 'meta_keywords']
BLOG_SEO_ADMIN_SEARCH = ['post']

BLOG_TAG_ADMIN_LIST = ['name', 'slug', 'created_at', 'updated_at']
BLOG_TAG_ADMIN_FILTER = ['created_at', 'updated_at']
BLOG_TAG_ADMIN_SEARCH = ['name']
