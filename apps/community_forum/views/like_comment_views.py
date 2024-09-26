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
