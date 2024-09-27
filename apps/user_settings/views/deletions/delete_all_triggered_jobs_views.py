from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.mm_triggered_jobs.models import TriggeredJob
from apps.user_permissions.models import PermissionNames


class DeleteAllTriggeredJobsView(View, LoginRequiredMixin):
    """
    Handles the deletion of all triggered jobs associated with the user account.
    """

    def post(self, request, *args, **kwargs):
        user = request.user
        user_triggered_jobs = TriggeredJob.objects.filter(trigger_assistant__organization__users__in=[user]).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL TRIGGERED JOBS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL TRIGGERED JOBS'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_TRIGGERS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_TRIGGERS):
            messages.error(self.request, "You do not have permission to delete triggered jobs.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for triggered_job in user_triggered_jobs:
                triggered_job.delete()
            messages.success(request, "All triggered jobs associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting triggered jobs: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')
