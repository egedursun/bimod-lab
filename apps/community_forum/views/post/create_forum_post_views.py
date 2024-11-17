#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_forum_post_views.py
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

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import TemplateView

from apps.community_forum.forms import ForumPostForm
from apps.community_forum.models import ForumThread, ForumCategory
from apps.community_forum.utils import CONST_HOURS
from auth.utils import ForumRewardActionsNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class ForumView_PostCreate(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        thread_id = self.kwargs.get("thread_id")
        thread = get_object_or_404(ForumThread, id=thread_id)

        try:
            if request.user.profile.user_last_forum_post_at:
                if (timezone.now() - request.user.profile.user_last_forum_post_at).seconds < (1 * CONST_HOURS):
                    messages.error(request, "You can only post once per hour.")
                    logger.error(f"User tried to post more than once per hour. User ID: {request.user.id}")
                    return redirect('community_forum:thread_detail', thread_id=thread.id)

            request.user.profile.user_last_forum_post_at = timezone.now()
            request.user.profile.save()
            form = ForumPostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.thread = thread
                post.created_by = request.user
                post.save()
                request.user.profile.add_points(ForumRewardActionsNames.ASK_QUESTION)
                logger.info(f"Forum post created. Post ID: {post.id}")
                return redirect('community_forum:thread_detail', thread_id=thread.id)
        except Exception as e:
            logger.error(f"Error creating forum post: {e}")
            messages.error(request, "An error occurred while creating the post.")
            return redirect('community_forum:thread_detail', thread_id=thread.id)

        context = self.get_context_data(**kwargs)
        context['form'] = form
        logger.error(f"Error creating forum post: {form.errors}")
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        thread_id = self.kwargs.get("thread_id")

        try:
            thread = get_object_or_404(ForumThread, id=thread_id)
            categories = ForumCategory.objects.prefetch_related(
                Prefetch('threads', queryset=ForumThread.objects.order_by('-created_at'))
            )
            context['categories'] = categories
            context['thread'] = thread
            context['form'] = ForumPostForm()
        except Exception as e:
            logger.error(f"Error getting context data for forum post creation: {e}")
            return context

        return context
