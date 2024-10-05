#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

#
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.mm_triggered_jobs.forms import TriggeredJobForm
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class CreateTriggeredJobView(LoginRequiredMixin, TemplateView):
    """
    Handles the creation of new triggered jobs.

    This view allows users to create triggered jobs that are associated with an assistant and can be executed based on specific events. The view checks user permissions before allowing the creation of a new triggered job.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with the form for creating a triggered job.
        post(self, request, *args, **kwargs): Processes the form submission to create a new triggered job.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['form'] = TriggeredJobForm()
        return context

    def post(self, request, *args, **kwargs):
        form = TriggeredJobForm(request.POST)

        ##############################
        # PERMISSION CHECK FOR - ADD_TRIGGERS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_TRIGGERS):
            messages.error(self.request, "You do not have permission to add triggered jobs.")
            return redirect('mm_triggered_jobs:list')
        ##############################

        if form.is_valid():
            triggered_job = form.save(commit=False)
            triggered_job.created_by_user = request.user
            # Handle dynamic fields
            step_guide = request.POST.getlist('step_guide[]')
            triggered_job.step_guide = step_guide
            triggered_job.save()
            messages.success(request, "Triggered Job created successfully!")
            print('[CreateTriggeredJobView.post] Triggered Job created successfully.')
            return redirect('mm_triggered_jobs:list')
        else:
            messages.error(request, "There was an error creating the triggered job.")
            return self.render_to_response({'form': form})
