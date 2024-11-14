#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_orchestration_scheduled_jobs_views.py
#  Last Modified: 2024-11-14 06:15:54
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-14 06:15:54
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
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.mm_scheduled_jobs.models import OrchestrationScheduledJob
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class ScheduledJobView_OrchestrationDelete(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        scheduled_job_id = self.kwargs.get('pk')
        scheduled_job = get_object_or_404(OrchestrationScheduledJob, id=scheduled_job_id)
        context['scheduled_job'] = scheduled_job
        return context

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - DELETE_ORCHESTRATION_SCHEDULED_JOBS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_ORCHESTRATION_SCHEDULED_JOBS):
            messages.error(self.request, "You do not have permission to delete Orchestration scheduled jobs.")
            return redirect('mm_scheduled_jobs:orchestration_list')
        ##############################

        scheduled_job_id = self.kwargs.get('pk')
        scheduled_job = get_object_or_404(OrchestrationScheduledJob, id=scheduled_job_id)
        scheduled_job.delete()
        logger.info(f"Orchestration Scheduled Job was deleted by User: {self.request.user.id}.")
        messages.success(request, "Orchestration Scheduled Job deleted successfully.")
        return redirect('mm_scheduled_jobs:orchestration_list')
