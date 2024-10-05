#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.mm_scheduled_jobs.forms import ScheduledJobForm
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class CreateScheduledJobView(LoginRequiredMixin, TemplateView):
    """
    Handles the creation of new scheduled jobs.

    This view allows users to create scheduled jobs that can be executed by their assistants. The view checks user permissions before allowing the creation of a new scheduled job.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with the form for creating a scheduled job.
        post(self, request, *args, **kwargs): Processes the form submission to create a new scheduled job and associates it with the user.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['form'] = ScheduledJobForm()
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
        if form.is_valid():
            scheduled_job = form.save(commit=False)
            scheduled_job.created_by_user = request.user
            # Handle dynamic fields
            step_guide = request.POST.getlist('step_guide[]')
            scheduled_job.step_guide = step_guide
            scheduled_job.save()
            print('[CreateScheduledJobView.post] Scheduled Job created successfully.')
            messages.success(request, "Scheduled Job created successfully!")
            return redirect('mm_scheduled_jobs:list')
        else:
            messages.error(request, "There was an error creating the scheduled job.")
            return self.render_to_response({'form': form})
