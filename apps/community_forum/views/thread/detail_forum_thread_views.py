#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: detail_forum_thread_views.py
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
from django.core.paginator import Paginator
from django.db.models import Prefetch, Q
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import TemplateView

from apps.community_forum.forms import ForumCommentForm

from apps.community_forum.models import (
    ForumThread,
    ForumPost,
    ForumCategory,
    ForumComment,
    ForumLike
)

from apps.community_forum.utils import CONST_MINUTES
from auth.utils import ForumRewardActionsNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class ForumView_ThreadDetail(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        thread_id = self.kwargs.get("thread_id")
        thread = get_object_or_404(ForumThread, id=thread_id)

        try:
            post_id = request.POST.get("post_id")
            post = get_object_or_404(ForumPost, id=post_id)

            if request.user.profile.user_last_forum_comment_at:
                if (timezone.now() - request.user.profile.user_last_forum_comment_at).seconds < (5 * CONST_MINUTES):
                    messages.error(request, "You can only comment once every 5 minutes.")
                    logger.error(f"User tried to comment more than once per 5 minutes. User ID: {request.user.id}")
                    return redirect('community_forum:thread_detail', thread_id=thread.id)

            request.user.profile.user_last_forum_comment_at = timezone.now()
            request.user.profile.save()

        except Exception as e:
            logger.error(f"Error creating forum comment: {e}")
            messages.error(request, "An error occurred while creating the comment.")
            return redirect('community_forum:thread_detail', thread_id=thread.id)

        try:
            form = ForumCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.created_by = request.user
                comment.save()

                request.user.profile.add_points(ForumRewardActionsNames.ADD_COMMENT)
                logger.info(f"Forum comment created. Comment ID: {comment.id}")
                return redirect('community_forum:thread_detail', thread_id=thread.id)

        except Exception as e:
            logger.error(f"Error creating forum comment: {e}")
            messages.error(request, "An error occurred while creating the comment.")
            return redirect('community_forum:thread_detail', thread_id=thread.id)

        context = self.get_context_data(**kwargs)
        context['form'] = form
        logger.error(f"Error creating forum comment: {form.errors}")
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        thread_id = self.kwargs.get("thread_id")

        try:
            thread = get_object_or_404(ForumThread, id=thread_id)
            context['thread'] = thread
            categories = ForumCategory.objects.prefetch_related(
                Prefetch('threads', queryset=ForumThread.objects.order_by('-created_at'))
            )

            context['categories'] = categories
            search_query = self.request.GET.get('search', '')

            if search_query:
                posts = thread.posts.filter(
                    Q(content__icontains=search_query) |
                    Q(comments__content__icontains=search_query)
                ).distinct().order_by('created_at')

            else:
                posts = thread.posts.all().order_by('created_at')

        except Exception as e:
            logger.error(f"Error getting context data for forum thread detail: {e}")
            return context

        try:
            post_paginator = Paginator(posts, 5)
            page_number = self.request.GET.get('page')
            page_obj = post_paginator.get_page(page_number)
            context['posts'] = page_obj
            context['post_page_obj'] = page_obj
            context['search_query'] = search_query

            for post in context['posts']:
                comments = ForumComment.objects.filter(
                    post=post
                ).order_by('created_at')

                comment_paginator = Paginator(comments, 5)
                comment_page_number = self.request.GET.get(f'comment_page_{post.id}')
                post.ordered_comments = comment_paginator.get_page(comment_page_number)
                post.comment_page_obj = post.ordered_comments

                for comment in post.ordered_comments:
                    comment.user_has_liked = ForumLike.objects.filter(
                        comment=comment,
                        user=self.request.user
                    ).exists()

        except Exception as e:
            logger.error(f"Error paginating posts and comments: {e}")
            return context

        context['form'] = ForumCommentForm()
        logger.info(f"Thread detail view accessed. Thread ID: {thread.id}")
        return context
