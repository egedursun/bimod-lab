#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: verify_forum_comment_views.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:39
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: verify_forum_comment_views.py
#  Last Modified: 2024-09-26 22:02:31
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:22:21
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from apps.community_forum.models import ForumPost, ForumComment
from auth.models import ForumRewardActionsNames


class ForumVerifyCommentView(LoginRequiredMixin, View):
    """
    Allows the thread owner to verify a specific comment on a post as the merited answer.

    Verifying a comment awards points to the comment owner and removes points from the previously verified comment owner if applicable.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles the verification of a comment on a specific post.

        Returns:
            HttpResponseRedirect: Redirects to the thread detail view after the comment is verified.
        """
        post_id = self.kwargs.get("post_id")
        comment_id = self.kwargs.get("comment_id")
        post = get_object_or_404(ForumPost, id=post_id)
        comment = get_object_or_404(ForumComment, id=comment_id)

        # check if there was an existing comment that is merited
        if post.is_verified:
            # Remove POINTS for getting a merit to the user who owns the comment
            comment_owner = post.verified_comment.created_by
            comment_owner.profile.remove_points(ForumRewardActionsNames.GET_MERIT)

        if post.created_by == request.user:
            post.verify_comment(comment)

        # Add POINTS for getting a merit to the user who owns the comment
        comment_owner = comment.created_by
        comment_owner.profile.add_points(ForumRewardActionsNames.GET_MERIT)

        return redirect('community_forum:thread_detail', thread_id=post.thread.id)
