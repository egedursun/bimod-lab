#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: list_triggered_jobs_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:45
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

#
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.mm_triggered_jobs.models import TriggeredJob
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class ListTriggeredJobsView(LoginRequiredMixin, TemplateView):
    """
    Displays a list of triggered jobs associated with the user's assistants.

    This view retrieves and displays all triggered jobs that are available to the current user, with support for searching and pagination.

    Methods:
        get_context_data(self, **kwargs): Retrieves the user's accessible triggered jobs and adds them to the context.
    """

    paginate_by = 10  # Adjust the number of items per page

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_TRIGGERS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_TRIGGERS):
            messages.error(self.request, "You do not have permission to list triggered jobs.")
            return context
        ##############################

        search_query = self.request.GET.get('search', '')
        user_organizations = self.request.user.organizations.all()
        organization_assistants = user_organizations.values_list('assistants', flat=True)
        triggered_jobs_list = TriggeredJob.objects.filter(trigger_assistant__in=organization_assistants)

        if search_query:
            triggered_jobs_list = triggered_jobs_list.filter(
                Q(name__icontains=search_query) | Q(task_description__icontains=search_query)
            )
        paginator = Paginator(triggered_jobs_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['triggered_jobs'] = page_obj.object_list
        context['total_triggered_jobs'] = TriggeredJob.objects.count()
        context['search_query'] = search_query
        return context
