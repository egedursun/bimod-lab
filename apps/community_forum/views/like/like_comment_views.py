#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: like_comment_views.py
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
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import View

from apps.community_forum.models import ForumComment, ForumLike
from auth.models import ForumRewardActionsNames


class LikeCommentView(LoginRequiredMixin, View):
    """
    Allows users to like or unlike a comment on a post.

    Liking a comment awards points to the comment owner, and unliking removes the points.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles the liking or unliking of a comment.

        Returns:
            HttpResponseRedirect: Redirects to the previous page after the like action.
        """
        comment_id = self.kwargs.get("comment_id")
        comment = get_object_or_404(ForumComment, id=comment_id)

        # Check if the user has already liked the comment
        like, created = ForumLike.objects.get_or_create(user=request.user, comment=comment)

        if not created:
            # User already liked this comment, so we remove the like
            like.delete()
            comment.like_count -= 1
            comment.save()

            # Remove POINTS for getting a like to the user who owns the comment
            comment_owner = comment.created_by
            comment_owner.profile.remove_points(ForumRewardActionsNames.GET_LIKE)
        else:
            # New like created
            comment.like_count += 1
            comment.save()

            # Add POINTS for getting a like to the user who owns the comment
            comment_owner = comment.created_by
            comment_owner.profile.add_points(ForumRewardActionsNames.GET_LIKE)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
