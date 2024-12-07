#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_triggered_job_views.py
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
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.mm_triggered_jobs.models import TriggeredJob
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class TriggeredJobView_Delete(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        triggered_job_id = self.kwargs.get('pk')

        triggered_job = get_object_or_404(
            TriggeredJob,
            id=triggered_job_id
        )

        context['triggered_job'] = triggered_job
        return context

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - DELETE_TRIGGERS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_TRIGGERS
        ):
            messages.error(self.request, "You do not have permission to delete triggered jobs.")
            return redirect('mm_triggered_jobs:list')
        ##############################

        triggered_job_id = self.kwargs.get('pk')

        triggered_job = get_object_or_404(
            TriggeredJob,
            id=triggered_job_id
        )

        try:
            triggered_job.delete()

        except Exception as e:
            messages.error(request, "An error occurred while deleting the Triggered Job: " + str(e))
            return redirect("mm_triggered_jobs:list")

        logger.info(f"Triggered Job was deleted by User: {self.request.user.id}.")
        messages.success(request, "Triggered Job deleted successfully.")

        return redirect('mm_triggered_jobs:list')
