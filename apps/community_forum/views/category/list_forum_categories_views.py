#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: list_forum_categories_views.py
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.views.generic import TemplateView

from apps.community_forum.models import ForumCategory
from web_project import TemplateLayout


class ForumView_CategoryList(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        search_query = self.request.GET.get('search', '')
        if search_query:
            categories = ForumCategory.objects.filter(threads__title__icontains=search_query).order_by("created_at")
        else:
            categories = ForumCategory.objects.all().order_by("created_at")

        paginator = Paginator(categories, 20)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['categories'] = page_obj
        context['page_obj'] = page_obj
        context['search_query'] = search_query
        return context
