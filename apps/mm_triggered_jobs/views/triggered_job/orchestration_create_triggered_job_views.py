#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: orchestration_create_triggered_job_views.py
#  Last Modified: 2024-11-14 07:21:09
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-14 07:21:10
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
from apps.mm_triggered_jobs.forms import OrchestrationTriggeredJobForm
from apps.mm_triggered_jobs.models import OrchestrationTriggeredJob
from apps.orchestrations.models import Maestro
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class TriggeredJobView_OrchestrationCreate(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['form'] = OrchestrationTriggeredJobForm()
        user_orgs = Organization.objects.filter(users__in=[self.request.user])
        trigger_maestros = Maestro.objects.filter(organization__in=user_orgs)
        context['trigger_maestros'] = trigger_maestros
        return context

    def post(self, request, *args, **kwargs):
        form = OrchestrationTriggeredJobForm(request.POST)

        ##############################
        # PERMISSION CHECK FOR - ADD_ORCHESTRATION_TRIGGERS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_ORCHESTRATION_TRIGGERS):
            messages.error(self.request, "You do not have permission to add orchestration triggered jobs.")
            return redirect('mm_triggered_jobs:orchestration_list')
        ##############################

        if form.is_valid():
            triggered_job: OrchestrationTriggeredJob = form.save(commit=False)
            maestro_id = request.POST.get('trigger_maestro')
            trigger_maestro = Maestro.objects.get(id=maestro_id)
            triggered_job.created_by_user = request.user
            step_guide = request.POST.getlist('step_guide[]')
            triggered_job.step_guide = step_guide
            triggered_job.trigger_maestro = trigger_maestro
            triggered_job.save()
            logger.info(f"Triggered Job was created by User: {self.request.user.id}.")
            messages.success(request, "Orchestration Triggered Job created successfully!")
            return redirect('mm_triggered_jobs:orchestration_list')
        else:
            logger.error(f"Error creating orchestration triggered job: {form.errors}")
            messages.error(request, "There was an error creating the orchestration triggered job.")
            return self.render_to_response({'form': form})
