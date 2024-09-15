"""
This module contains views for managing forum categories, threads, posts, and comments within the community forum application.
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Prefetch, Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView

from apps.community_forum.forms import ForumPostForm, ForumCommentForm
from apps.community_forum.models import ForumCategory, ForumThread, ForumPost, ForumComment, ForumLike
from auth.models import ForumRewardActionsNames
from web_project import TemplateLayout


# Constants
SECONDS = 1
MINUTES = 60 * SECONDS
HOUR = 60 * MINUTES


class ForumCategoryListView(LoginRequiredMixin, TemplateView):
    """
    Displays a list of forum categories with support for pagination.
    """
    def get_context_data(self, **kwargs):
        """
        Retrieves and returns the context data for rendering the template.

        Returns:
            dict: Context data containing the paginated categories.
        """
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        search_query = self.request.GET.get('search', '')

        # Filter categories based on the search query
        if search_query:
            categories = ForumCategory.objects.filter(threads__title__icontains=search_query).order_by("created_at")
        else:
            categories = ForumCategory.objects.all().order_by("created_at")

        # Paginate categories, 20 per page
        paginator = Paginator(categories, 20)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['categories'] = page_obj
        context['page_obj'] = page_obj
        context['search_query'] = search_query
        return context


class ForumThreadListView(LoginRequiredMixin, TemplateView):
    """
    Displays a list of threads within a specific category with support for pagination.
    """
    def get_context_data(self, **kwargs):
        """
        Retrieves and returns the context data for rendering the template.

        Returns:
            dict: Context data containing the category and paginated threads.
        """
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        category_slug = self.kwargs.get("slug")
        category = get_object_or_404(ForumCategory, slug=category_slug)
        context['category'] = category

        # Prefetch threads for each category
        categories = ForumCategory.objects.prefetch_related(
            Prefetch('threads', queryset=ForumThread.objects.order_by('-created_at'))
        )
        context['categories'] = categories

        # Handle the search functionality
        search_query = self.request.GET.get('search', '')
        if search_query:
            threads = category.threads.filter(
                Q(title__icontains=search_query)
            ).order_by('-created_at')
        else:
            threads = category.threads.all().order_by('-created_at')

        # Paginate threads, 10 per page
        paginator = Paginator(threads, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['threads'] = page_obj
        context['page_obj'] = page_obj
        context['search_query'] = search_query
        return context


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


class ForumPostCreateView(LoginRequiredMixin, TemplateView):
    """
    Allows users to create a new post within a thread.

    Ensures that users can only post once per hour and awards points for creating new posts.
    """
    def post(self, request, *args, **kwargs):
        """
        Handles the creation of a new post in a specific thread.

        Ensures that users can only post once per hour.

        Returns:
            HttpResponseRedirect: Redirects to the thread detail view after the post is created.
        """
        thread_id = self.kwargs.get("thread_id")
        thread = get_object_or_404(ForumThread, id=thread_id)

        if request.user.profile.user_last_forum_post_at:
            # Check if the user has posted in the last hour
            if (timezone.now() - request.user.profile.user_last_forum_post_at).seconds < (1 * HOUR):
                messages.error(request, "You can only post once per hour.")
                return redirect('community_forum:thread_detail', thread_id=thread.id)

        # save the last post time to the user's profile
        request.user.profile.user_last_forum_post_at = timezone.now()
        request.user.profile.save()

        form = ForumPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.thread = thread
            post.created_by = request.user
            post.save()

            # Add POINTS for asking a question to the user
            request.user.profile.add_points(ForumRewardActionsNames.ASK_QUESTION)

            return redirect('community_forum:thread_detail', thread_id=thread.id)

        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        """
        Retrieves and returns the context data for rendering the post creation template.

        Returns:
            dict: Context data containing the thread details and the post form.
        """
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        thread_id = self.kwargs.get("thread_id")
        thread = get_object_or_404(ForumThread, id=thread_id)

        # Prefetch threads for each category
        categories = ForumCategory.objects.prefetch_related(
            Prefetch('threads', queryset=ForumThread.objects.order_by('-created_at'))
        )
        context['categories'] = categories

        context['thread'] = thread
        context['form'] = ForumPostForm()
        return context


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
