#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
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

from django.urls import path

from apps.blog_app.views import (
    BlogPostView_List,
    BlogPostView_Detail
)

app_name = 'blog_app'

urlpatterns = [
    path(
        '',
        BlogPostView_List.as_view(
            template_name='blog_app/blogpost_list.html'
        ),
        name='post_list'
    ),

    path(
        'post/<slug:slug>/',
        BlogPostView_Detail.as_view(
            template_name='blog_app/blogpost_detail.html'
        ),
        name='post_detail'
    ),
]
