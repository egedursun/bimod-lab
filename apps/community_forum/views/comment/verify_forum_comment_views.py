#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: verify_forum_comment_views.py
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

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from apps.community_forum.models import ForumPost, ForumComment
from auth.utils import ForumRewardActionsNames


class ForumView_CommentVerify(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post_id = self.kwargs.get("post_id")
        comment_id = self.kwargs.get("comment_id")
        post = get_object_or_404(ForumPost, id=post_id)
        comment = get_object_or_404(ForumComment, id=comment_id)
        if post.is_verified:
            comment_owner = post.verified_comment.created_by
            comment_owner.profile.remove_points(ForumRewardActionsNames.GET_MERIT)
        if post.created_by == request.user:
            post.verify_comment(comment)
        comment_owner = comment.created_by
        comment_owner.profile.add_points(ForumRewardActionsNames.GET_MERIT)
        return redirect('community_forum:thread_detail', thread_id=post.thread.id)
