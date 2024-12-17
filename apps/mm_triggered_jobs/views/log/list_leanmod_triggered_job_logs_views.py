#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_leanmod_triggered_job_logs_views.py
#  Last Modified: 2024-12-07 17:21:18
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-07 17:21:19
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

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.mm_triggered_jobs.models import (
    LeanModTriggeredJob,
    LeanModTriggeredJobInstance
)

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class TriggeredJobView_LeanModLogList(LoginRequiredMixin, TemplateView):
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_LEANMOD_TRIGGERS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.LIST_LEANMOD_TRIGGERS
        ):
            messages.error(self.request, "You do not have permission to list LeanMod triggered jobs.")

            return context
        ##############################

        triggered_job_id = self.kwargs.get('pk')

        triggered_job = get_object_or_404(
            LeanModTriggeredJob,
            id=triggered_job_id
        )

        context['triggered_job'] = triggered_job
        search_query = self.request.GET.get('search', '')

        job_instances_list = LeanModTriggeredJobInstance.objects.filter(
            triggered_job=triggered_job
        )

        if search_query:
            job_instances_list = job_instances_list.filter(
                Q(status__icontains=search_query) |
                Q(logs__icontains=search_query) |
                Q(triggered_job__name__icontains=search_query)
            )

        paginator = Paginator(job_instances_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        context['triggered_job_instances'] = page_obj.object_list
        context['total_triggered_job_instances'] = job_instances_list.count()
        context['search_query'] = search_query

        logger.info(f"LeanMod Triggered Job Log List View accessed by User: {self.request.user.id}.")

        return context
