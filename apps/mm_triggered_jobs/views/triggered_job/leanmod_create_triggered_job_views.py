#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: leanmod_create_triggered_job_views.py
#  Last Modified: 2024-12-07 17:25:30
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-07 17:25:31
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

from apps.mm_triggered_jobs.forms import (
    LeanModTriggeredJobForm
)
from apps.mm_triggered_jobs.models import (
    LeanModTriggeredJob
)

from apps.organization.models import Organization

from apps.user_permissions.utils import (
    PermissionNames
)

from config.settings import (
    MAX_TRIGGERED_JOBS_PER_LEANMOD
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class TriggeredJobView_LeanModCreate(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        context['form'] = LeanModTriggeredJobForm()

        user_orgs = Organization.objects.filter(
            users__in=[self.request.user]
        )

        trigger_leanmods = LeanAssistant.objects.filter(
            organization__in=user_orgs
        )

        context['trigger_leanmods'] = trigger_leanmods
        return context

    def post(self, request, *args, **kwargs):
        form = LeanModTriggeredJobForm(request.POST)

        ##############################
        # PERMISSION CHECK FOR - ADD_LEANMOD_TRIGGERS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.ADD_LEANMOD_TRIGGERS
        ):
            messages.error(self.request, "You do not have permission to add LeanMod triggered jobs.")

            return redirect('mm_triggered_jobs:leanmod_list')
        ##############################

        if form.is_valid():

            triggered_job: LeanModTriggeredJob = form.save(
                commit=False
            )

            leanmod_id = request.POST.get('trigger_leanmod')

            trigger_leanmod = LeanAssistant.objects.get(
                id=leanmod_id
            )

            n_triggered_jobs = trigger_leanmod.triggered_jobs.count()

            if n_triggered_jobs > MAX_TRIGGERED_JOBS_PER_LEANMOD:
                messages.error(
                    request,
                    f'LeanMod agent has reached the maximum number of connected triggered jobs ({MAX_TRIGGERED_JOBS_PER_LEANMOD}).'
                )

                return redirect('mm_triggered_jobs:leanmod_list')

            triggered_job.created_by_user = request.user
            step_guide = request.POST.getlist('step_guide[]')

            triggered_job.step_guide = step_guide
            triggered_job.trigger_leanmod = trigger_leanmod

            triggered_job.save()

            logger.info(f"LeanMod Triggered Job was created by User: {self.request.user.id}.")
            messages.success(request, "LeanMod Triggered Job created successfully!")

            return redirect('mm_triggered_jobs:leanmod_list')

        else:
            logger.error(f"Error creating LeanMod triggered job: {form.errors}")
            messages.error(request, "There was an error creating the LeanMod triggered job.")

            return self.render_to_response(
                {
                    'form': form
                }
            )
