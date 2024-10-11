#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: urls.py
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

from django.urls import path
from . import views
from .views import ForumView_CommentLike

app_name = 'community_forum'

urlpatterns = [
    path('categories/', views.ForumView_CategoryList.as_view(
        template_name='community_forum/category_list.html'), name='category_list'),
    path('category/<slug:slug>/', views.ForumView_ThreadList.as_view(
        template_name='community_forum/thread_list.html'
    ), name='thread_list'),
    path('thread/<int:thread_id>/', views.ForumView_ThreadDetail.as_view(
        template_name='community_forum/thread_detail.html'
    ), name='thread_detail'),
    path('thread/<int:thread_id>/create_post/', views.ForumView_PostCreate.as_view(
        template_name='community_forum/post_create.html'
    ), name='post_create'),
    path('post/<int:post_id>/verify_comment/<int:comment_id>/', views.ForumView_CommentVerify.as_view(),
         name='verify_comment'),
    path('comment/<int:comment_id>/like/', ForumView_CommentLike.as_view(), name='like_comment'),
]
