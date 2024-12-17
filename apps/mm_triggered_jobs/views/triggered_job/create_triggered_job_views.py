#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_triggered_job_views.py
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
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging

from django.contrib import messages

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.assistants.models import Assistant
from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.mm_triggered_jobs.forms import TriggeredJobForm
from apps.mm_triggered_jobs.models import TriggeredJob
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from config.settings import MAX_TRIGGERED_JOBS_PER_ASSISTANT
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class TriggeredJobView_Create(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['form'] = TriggeredJobForm()

        user_orgs = Organization.objects.filter(
            users__in=[self.request.user]
        )

        trigger_assistants = Assistant.objects.filter(
            organization__in=user_orgs
        )

        context['trigger_assistants'] = trigger_assistants

        return context

    def post(self, request, *args, **kwargs):
        form = TriggeredJobForm(request.POST)

        ##############################
        # PERMISSION CHECK FOR - ADD_TRIGGERS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.ADD_TRIGGERS
        ):
            messages.error(self.request, "You do not have permission to add triggered jobs.")
            return redirect('mm_triggered_jobs:list')
        ##############################

        if form.is_valid():

            triggered_job: TriggeredJob = form.save(
                commit=False
            )

            assistant_id = request.POST.get('trigger_assistant')

            trigger_assistant = Assistant.objects.get(
                id=assistant_id
            )

            n_triggered_jobs = trigger_assistant.triggered_jobs.count()

            if n_triggered_jobs > MAX_TRIGGERED_JOBS_PER_ASSISTANT:
                messages.error(request,
                               f'Assistant has reached the maximum number of connected triggered jobs ({MAX_TRIGGERED_JOBS_PER_ASSISTANT}).')

                return redirect('mm_triggered_jobs:list')

            triggered_job.created_by_user = request.user
            step_guide = request.POST.getlist('step_guide[]')

            triggered_job.step_guide = step_guide
            triggered_job.trigger_assistant = trigger_assistant

            triggered_job.save()

            logger.info(f"Triggered Job was created by User: {self.request.user.id}.")
            messages.success(request, "Triggered Job created successfully!")

            return redirect('mm_triggered_jobs:list')

        else:
            logger.error(f"Error creating triggered job: {form.errors}")
            messages.error(request, "There was an error creating the triggered job.")

            return self.render_to_response(
                {
                    'form': form
                }
            )
