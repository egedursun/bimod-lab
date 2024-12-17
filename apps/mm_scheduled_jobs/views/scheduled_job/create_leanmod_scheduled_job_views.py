#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_leanmod_scheduled_job_views.py
#  Last Modified: 2024-12-07 13:53:53
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-07 13:53:55
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

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.leanmod.models import LeanAssistant

from apps.mm_scheduled_jobs.forms import (
    LeanModScheduledJobForm
)

from apps.organization.models import Organization

from apps.user_permissions.utils import (
    PermissionNames
)

from config.settings import (
    MAX_SCHEDULED_JOBS_PER_LEANMOD
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class ScheduledJobView_LeanModCreate(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['form'] = LeanModScheduledJobForm()
        context["user"] = self.request.user

        user_orgs = Organization.objects.filter(
            users__in=[self.request.user]
        )

        context['leanmods'] = LeanAssistant.objects.filter(
            organization__in=user_orgs
        )

        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - ADD_LEANMOD_SCHEDULED_JOBS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.ADD_LEANMOD_SCHEDULED_JOBS
        ):
            messages.error(self.request, "You do not have permission to add LeanMod scheduled jobs.")
            return redirect('mm_scheduled_jobs:leanmod_list')
        ##############################

        form = LeanModScheduledJobForm(request.POST)

        leanmod_id = request.POST.get('leanmod')

        leanmod = LeanAssistant.objects.get(
            id=leanmod_id
        )

        if form.is_valid():

            n_scheduled_jobs = leanmod.scheduled_jobs.count()

            if n_scheduled_jobs > MAX_SCHEDULED_JOBS_PER_LEANMOD:
                messages.error(
                    request,
                    f'LeanMod assistant has reached the maximum number of connected scheduled jobs ({MAX_SCHEDULED_JOBS_PER_LEANMOD}).'
                )

                return redirect('mm_scheduled_jobs:leanmod_list')

            scheduled_job = form.save(
                commit=False
            )

            scheduled_job.leanmod = leanmod
            scheduled_job.created_by_user = request.user

            step_guide = request.POST.getlist('step_guide[]')
            scheduled_job.step_guide = step_guide

            scheduled_job.save()

            logger.info(f"LeanMod Scheduled Job was created by User: {self.request.user.id}.")
            messages.success(request, "LeanMod Scheduled Job created successfully!")

            return redirect('mm_scheduled_jobs:leanmod_list')

        else:
            logger.error(f"Error creating LeanMod Scheduled Job by User: {self.request.user.id}.")
            messages.error(request, "There was an error creating the LeanMod scheduled job.")

            return self.render_to_response(
                {
                    'form': form
                }
            )
