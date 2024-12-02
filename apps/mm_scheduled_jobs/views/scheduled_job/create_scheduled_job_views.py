#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_scheduled_job_views.py
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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.assistants.models import Assistant
from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.mm_scheduled_jobs.forms import ScheduledJobForm
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from config.settings import MAX_SCHEDULED_JOBS_PER_ASSISTANT
from web_project import TemplateLayout


logger = logging.getLogger(__name__)


class ScheduledJobView_Create(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['form'] = ScheduledJobForm()
        context["user"] = self.request.user
        user_orgs = Organization.objects.filter(users__in=[self.request.user])
        context['assistants'] = Assistant.objects.filter(organization__in=user_orgs)
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - ADD_SCHEDULED_JOBS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_SCHEDULED_JOBS):
            messages.error(self.request, "You do not have permission to add scheduled jobs.")
            return redirect('mm_scheduled_jobs:list')
        ##############################

        form = ScheduledJobForm(request.POST)

        assistant_id = request.POST.get('assistant')
        assistant = Assistant.objects.get(id=assistant_id)

        if form.is_valid():

            # check the number of scheduled jobs assistant has
            n_scheduled_jobs = assistant.scheduled_jobs.count()
            if n_scheduled_jobs > MAX_SCHEDULED_JOBS_PER_ASSISTANT:
                messages.error(request,
                               f'Assistant has reached the maximum number of connected scheduled jobs ({MAX_SCHEDULED_JOBS_PER_ASSISTANT}).')
                return redirect('mm_scheduled_jobs:list')

            scheduled_job = form.save(commit=False)
            scheduled_job.assistant = assistant
            scheduled_job.created_by_user = request.user

            step_guide = request.POST.getlist('step_guide[]')
            scheduled_job.step_guide = step_guide
            scheduled_job.save()

            logger.info(f"Scheduled Job was created by User: {self.request.user.id}.")
            messages.success(request, "Scheduled Job created successfully!")
            return redirect('mm_scheduled_jobs:list')

        else:
            logger.error(f"Error creating Scheduled Job by User: {self.request.user.id}: {form.errors}")
            messages.error(request, "There was an error creating the scheduled job.")
            return self.render_to_response({'form': form})
