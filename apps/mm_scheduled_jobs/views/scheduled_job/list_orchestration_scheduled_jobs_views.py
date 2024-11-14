#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_orchestration_scheduled_jobs_views.py
#  Last Modified: 2024-11-14 06:16:03
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-14 06:16:04
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
from django.db.models import Q
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.mm_scheduled_jobs.models import OrchestrationScheduledJob
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class ScheduledJobView_OrchestrationList(LoginRequiredMixin, TemplateView):
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_ORCHESTRATION_SCHEDULED_JOBS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_ORCHESTRATION_SCHEDULED_JOBS):
            messages.error(self.request, "You do not have permission to list Orchestration scheduled jobs.")
            return context
        ##############################

        search_query = self.request.GET.get('search', '')
        user_orgs = self.request.user.organizations.all()
        org_orchestrators = user_orgs.values_list('maestros', flat=True)
        scheduled_jobs_list = OrchestrationScheduledJob.objects.filter(maestro__in=org_orchestrators)
        if search_query:
            scheduled_jobs_list = scheduled_jobs_list.filter(
                Q(name__icontains=search_query) | Q(task_description__icontains=search_query))
        paginator = Paginator(scheduled_jobs_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['scheduled_jobs'] = page_obj.object_list
        context['total_scheduled_jobs'] = OrchestrationScheduledJob.objects.count()
        context['search_query'] = search_query
        logger.info(f"Orchestration Scheduled Jobs list was fetched by User: {self.request.user.id}.")
        return context
