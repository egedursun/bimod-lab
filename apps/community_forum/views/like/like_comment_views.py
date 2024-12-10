#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import View

from apps.community_forum.models import (
    ForumComment,
    ForumLike
)

from auth.utils import ForumRewardActionsNames

logger = logging.getLogger(__name__)


class ForumView_CommentLike(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        comment_id = self.kwargs.get("comment_id")

        comment = get_object_or_404(ForumComment, id=comment_id)

        try:
            like, created = ForumLike.objects.get_or_create(
                user=request.user,
                comment=comment
            )

            if not created:
                like.delete()
                comment.like_count -= 1

                comment.save()

                comment_owner = comment.created_by
                comment_owner.profile.remove_points(ForumRewardActionsNames.GET_LIKE)

            else:
                comment.like_count += 1

                comment.save()

                comment_owner = comment.created_by
                comment_owner.profile.add_points(ForumRewardActionsNames.GET_LIKE)

        except Exception as e:
            logger.error(f"[ForumView_CommentLike] Error liking the Comment: {e}")

            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        logger.info(f"Comment liked. Comment ID: {comment.id}")

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
