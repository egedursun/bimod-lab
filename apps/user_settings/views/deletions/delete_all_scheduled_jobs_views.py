from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.mm_scheduled_jobs.models import ScheduledJob
from apps.user_permissions.utils import PermissionNames


class DeleteAllScheduledJobsView(View, LoginRequiredMixin):
    """
    Handles the deletion of all scheduled jobs associated with the user account.
    """

    def post(self, request, *args, **kwargs):
        user = request.user
        user_scheduled_jobs = ScheduledJob.objects.filter(assistant__organization__users__in=[user]).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL SCHEDULED JOBS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL SCHEDULED JOBS'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_SCHEDULED_JOBS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_SCHEDULED_JOBS):
            messages.error(self.request, "You do not have permission to delete scheduled jobs.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for scheduled_job in user_scheduled_jobs:
                scheduled_job.delete()
            messages.success(request, "All scheduled jobs associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting scheduled jobs: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')
