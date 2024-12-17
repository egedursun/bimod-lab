#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_all_triggered_jobs_orchestration_views.py
#  Last Modified: 2024-11-24 23:42:55
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-24 23:42:56
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
from django.views import View

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)
from apps.mm_triggered_jobs.models import (
    OrchestrationTriggeredJob
)

from apps.user_permissions.utils import (
    PermissionNames
)

logger = logging.getLogger(__name__)


class SettingsView_DeleteAllOrchestrationTriggeredJobs(View, LoginRequiredMixin):

    def post(self, request, *args, **kwargs):
        user = request.user

        user_orchestration_triggered_jobs = OrchestrationTriggeredJob.objects.filter(
            trigger_maestro__organization__users__in=[user]
        ).all()

        confirmation_field = request.POST.get('confirmation', None)

        if confirmation_field != 'CONFIRM DELETING ALL ORCHESTRATION TRIGGERED JOBS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL ORCHESTRATION TRIGGERED JOBS'.")
            logger.error(f"Invalid confirmation field: {confirmation_field}")

            return redirect('user_settings:settings')

        ##############################
        # PERMISSION CHECK FOR - DELETE_ORCHESTRATION_TRIGGERS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_ORCHESTRATION_TRIGGERS
        ):
            messages.error(self.request, "You do not have permission to delete Orchestration triggered jobs.")

            return redirect('user_settings:settings')
        ##############################

        try:
            for orchestration_triggered_job in user_orchestration_triggered_jobs:
                orchestration_triggered_job.delete()

            messages.success(request,
                             "All Orchestration triggered jobs associated with your account have been deleted.")

            logger.info(f"All Orchestration triggered jobs associated with User: {user.id} have been deleted.")

        except Exception as e:
            messages.error(request, f"Error deleting Orchestration triggered jobs: {e}")
            logger.error(f"Error deleting Orchestration triggered jobs: {e}")

        return redirect('user_settings:settings')
