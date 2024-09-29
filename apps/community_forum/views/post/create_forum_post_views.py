#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: create_forum_post_views.py
#  Last Modified: 2024-09-26 22:02:31
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:22:40
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import TemplateView

from apps.community_forum.forms import ForumPostForm
from apps.community_forum.models import ForumThread, ForumCategory
from apps.community_forum.utils import HOURS
from auth.models import ForumRewardActionsNames
from web_project import TemplateLayout


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
            if (timezone.now() - request.user.profile.user_last_forum_post_at).seconds < (1 * HOURS):
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
