#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: list_forum_threads_views.py
#  Last Modified: 2024-09-26 22:02:31
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:22:53
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Prefetch, Q
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from apps.community_forum.models import ForumCategory, ForumThread
from web_project import TemplateLayout


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
