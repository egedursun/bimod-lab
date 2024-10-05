#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: delete_scheduled_jobs_views.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:43
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: delete_scheduled_jobs_views.py
#  Last Modified: 2024-09-28 16:44:41
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:02:30
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.mm_scheduled_jobs.models import ScheduledJob
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class ConfirmDeleteScheduledJobView(LoginRequiredMixin, TemplateView):
    """
    Handles the deletion of scheduled jobs.

    This view allows users to delete specific scheduled jobs, provided they have the necessary permissions.

    Methods:
        get_context_data(self, **kwargs): Prepares the context for the deletion confirmation page.
        post(self, request, *args, **kwargs): Processes the deletion of the specified scheduled job.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        scheduled_job_id = self.kwargs.get('pk')
        scheduled_job = get_object_or_404(ScheduledJob, id=scheduled_job_id)
        context['scheduled_job'] = scheduled_job
        return context

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - DELETE_SCHEDULED_JOBS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_SCHEDULED_JOBS):
            messages.error(self.request, "You do not have permission to delete scheduled jobs.")
            return redirect('mm_scheduled_jobs:list')
        ##############################

        scheduled_job_id = self.kwargs.get('pk')
        scheduled_job = get_object_or_404(ScheduledJob, id=scheduled_job_id)
        scheduled_job.delete()
        print('[ConfirmDeleteScheduledJobView.post] Scheduled Job deleted successfully.')
        messages.success(request, "Scheduled Job deleted successfully.")
        return redirect('mm_scheduled_jobs:list')
