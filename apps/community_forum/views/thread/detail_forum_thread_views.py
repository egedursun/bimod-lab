from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Prefetch, Q
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import TemplateView

from apps.community_forum.forms import ForumCommentForm
from apps.community_forum.models import ForumThread, ForumPost, ForumCategory, ForumComment, ForumLike
from apps.community_forum.utils import MINUTES
from auth.models import ForumRewardActionsNames
from web_project import TemplateLayout


class ForumThreadDetailView(LoginRequiredMixin, TemplateView):
    """
    Displays the details of a specific thread, including posts and their comments.
    Supports creating comments and paginates both posts and comments.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles the submission of a new comment on a specific post within the thread.

        Ensures that users can only comment once every 5 minutes.

        Returns:
            HttpResponseRedirect: Redirects to the thread detail view after the comment is posted.
        """
        thread_id = self.kwargs.get("thread_id")
        thread = get_object_or_404(ForumThread, id=thread_id)

        # Get the post the comment is for
        post_id = request.POST.get("post_id")
        post = get_object_or_404(ForumPost, id=post_id)

        # Check if the user has posted in the last 5 minutes
        if request.user.profile.user_last_forum_comment_at:
            if (timezone.now() - request.user.profile.user_last_forum_comment_at).seconds < (5 * MINUTES):
                messages.error(request, "You can only comment once every 5 minutes.")
                return redirect('community_forum:thread_detail', thread_id=thread.id)

        # If the user has never commented before, set the last comment time to now
        request.user.profile.user_last_forum_comment_at = timezone.now()
        request.user.profile.save()

        form = ForumCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.created_by = request.user
            comment.save()

            # Add POINTS for commenting to the commenting user
            request.user.profile.add_points(ForumRewardActionsNames.ADD_COMMENT)

            return redirect('community_forum:thread_detail', thread_id=thread.id)

        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        """
        Retrieves and returns the context data for rendering the thread detail template.

        Returns:
            dict: Context data containing the thread details, posts, comments, and pagination details.
        """
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        thread_id = self.kwargs.get("thread_id")
        thread = get_object_or_404(ForumThread, id=thread_id)
        context['thread'] = thread

        # Prefetch threads for each category
        categories = ForumCategory.objects.prefetch_related(
            Prefetch('threads', queryset=ForumThread.objects.order_by('-created_at'))
        )
        context['categories'] = categories

        # Handle the search functionality
        search_query = self.request.GET.get('search', '')
        if search_query:
            posts = thread.posts.filter(
                Q(content__icontains=search_query) | Q(comments__content__icontains=search_query)
            ).distinct().order_by('created_at')
        else:
            posts = thread.posts.all().order_by('created_at')

        # Paginate posts, 5 per page
        post_paginator = Paginator(posts, 5)
        page_number = self.request.GET.get('page')
        page_obj = post_paginator.get_page(page_number)
        context['posts'] = page_obj
        context['post_page_obj'] = page_obj
        context['search_query'] = search_query

        # Paginate comments for each post, 5 per page
        for post in context['posts']:
            comments = ForumComment.objects.filter(post=post).order_by('created_at')
            comment_paginator = Paginator(comments, 5)
            comment_page_number = self.request.GET.get(f'comment_page_{post.id}')
            post.ordered_comments = comment_paginator.get_page(comment_page_number)
            post.comment_page_obj = post.ordered_comments

            # Add user_like information for each comment
            for comment in post.ordered_comments:
                comment.user_has_liked = ForumLike.objects.filter(comment=comment, user=self.request.user).exists()

        context['form'] = ForumCommentForm()
        return context
