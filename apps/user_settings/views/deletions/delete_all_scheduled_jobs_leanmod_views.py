#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_all_scheduled_jobs_leanmod_views.py
#  Last Modified: 2024-12-07 18:18:57
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-07 18:18:57
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

from apps.mm_scheduled_jobs.models import (
    LeanModScheduledJob
)

from apps.user_permissions.utils import (
    PermissionNames
)

logger = logging.getLogger(__name__)


class SettingsView_DeleteAllLeanModScheduledJobs(View, LoginRequiredMixin):
    def post(self, request, *args, **kwargs):
        user = request.user

        user_leanmod_scheduled_jobs: LeanModScheduledJob = LeanModScheduledJob.objects.filter(
            leanmod__organization__users__in=[
                user
            ]
        ).all()

        confirmation_field = request.POST.get('confirmation', None)

        if confirmation_field != 'CONFIRM DELETING ALL LEANMOD SCHEDULED JOBS':
            messages.error(
                request,
                "Invalid confirmation field. Please confirm the deletion by typing "
                "exactly 'CONFIRM DELETING ALL LEANMOD SCHEDULED JOBS'."
            )

            logger.error(f"Invalid confirmation field: {confirmation_field}")

            return redirect('user_settings:settings')

        ##############################
        # PERMISSION CHECK FOR - DELETE_LEANMOD_SCHEDULED_JOBS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_LEANMOD_SCHEDULED_JOBS
        ):
            messages.error(self.request, "You do not have permission to delete LeanMod scheduled jobs.")

            return redirect('user_settings:settings')
        ##############################

        try:
            for leanmod_scheduled_job in user_leanmod_scheduled_jobs:
                leanmod_scheduled_job.delete()

            messages.success(request, "All LeanMod scheduled jobs associated with your account have been deleted.")
            logger.info(f"All LeanMod scheduled jobs associated with User: {user.id} have been deleted.")

        except Exception as e:
            messages.error(request, f"Error deleting LeanMod scheduled jobs: {e}")
            logger.error(f"Error deleting LeanMod scheduled jobs: {e}")

        return redirect('user_settings:settings')
