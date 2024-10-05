#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: list_forum_categories_views.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:39
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: list_forum_categories_views.py
#  Last Modified: 2024-09-26 22:02:31
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:22:14
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.views.generic import TemplateView

from apps.community_forum.models import ForumCategory
from web_project import TemplateLayout


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
