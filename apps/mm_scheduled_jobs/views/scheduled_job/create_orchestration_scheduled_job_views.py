#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_orchestration_scheduled_job_views.py
#  Last Modified: 2024-11-14 06:15:41
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-14 06:15:42
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
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.mm_scheduled_jobs.forms.orchestration_scheduled_job_forms import OrchestrationScheduledJobForm
from apps.orchestrations.models import Maestro
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


logger = logging.getLogger(__name__)


class ScheduledJobView_OrchestrationCreate(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['form'] = OrchestrationScheduledJobForm()
        context["user"] = self.request.user
        user_orgs = Organization.objects.filter(users__in=[self.request.user])
        context['maestros'] = Maestro.objects.filter(organization__in=user_orgs)
        logger.error(context['maestros'])
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - ADD_ORCHESTRATION_SCHEDULED_JOBS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_ORCHESTRATION_SCHEDULED_JOBS):
            messages.error(self.request, "You do not have permission to add orchestration scheduled jobs.")
            return redirect('mm_scheduled_jobs:orchestration_list')
        ##############################

        form = OrchestrationScheduledJobForm(request.POST)
        maestro_id = request.POST.get('maestro')
        maestro = Maestro.objects.get(id=maestro_id)
        if form.is_valid():
            scheduled_job = form.save(commit=False)
            scheduled_job.maestro = maestro
            scheduled_job.created_by_user = request.user
            step_guide = request.POST.getlist('step_guide[]')
            scheduled_job.step_guide = step_guide
            scheduled_job.save()
            logger.info(f"Orchestration Scheduled Job was created by User: {self.request.user.id}.")
            messages.success(request, "Orchestration Scheduled Job created successfully!")
            return redirect('mm_scheduled_jobs:orchestration_list')
        else:
            logger.error(f"Error creating Orchestration Scheduled Job by User: {self.request.user.id}.")
            messages.error(request, "There was an error creating the Orchestration scheduled job.")
            return self.render_to_response({'form': form})
