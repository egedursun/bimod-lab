#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_blog_posts_views.py
#  Last Modified: 2024-10-05 12:51:58
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:34
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
from django.db.models import Q
from django.views.generic import TemplateView

from apps.blog_app.models import BlogPost
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class BlogPostView_List(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        search_query = self.request.GET.get('search', '')

        if search_query:
            posts = BlogPost.objects.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(tags__name__icontains=search_query),
            ).order_by('-published_at')
        else:
            posts = BlogPost.objects.filter(status='published').order_by('-published_at')

        paginator = Paginator(posts, 9)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['search_query'] = search_query

        logger.info(f"Blog Posts were listed. User authenticated: {self.request.user.is_authenticated}")
        return context
