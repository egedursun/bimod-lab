#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_forum_threads_views.py
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
from django.core.paginator import Paginator
from django.db.models import Prefetch, Q
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from apps.community_forum.models import ForumCategory, ForumThread
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class ForumView_ThreadList(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        category_slug = self.kwargs.get("slug")

        try:
            category = get_object_or_404(ForumCategory, slug=category_slug)
            context['category'] = category
            categories = ForumCategory.objects.prefetch_related(
                Prefetch(
                    'threads',
                    queryset=ForumThread.objects.order_by('-created_at')
                )
            )

            context['categories'] = categories
            search_query = self.request.GET.get('search', '')

            if search_query:
                threads = category.threads.filter(
                    Q(title__icontains=search_query)
                ).order_by('-created_at')

            else:
                threads = category.threads.all().order_by('-created_at')

        except Exception as e:
            logger.error(f"[ForumView_ThreadList] Error listing the Forum Threads: {e}")
            return context

        try:
            paginator = Paginator(threads, 10)
            page_number = self.request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context['threads'] = page_obj
            context['page_obj'] = page_obj
            context['search_query'] = search_query

        except Exception as e:
            logger.error(f"[ForumView_ThreadList] Error listing the Forum Threads: {e}")
            return context

        return context
