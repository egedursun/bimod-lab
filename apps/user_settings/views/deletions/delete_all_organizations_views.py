from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames


class DeleteAllOrganizationsView(View, LoginRequiredMixin):
    """
    Handles the deletion of all organizations associated with the user account.
    """

    def post(self, request, *args, **kwargs):
        user = request.user
        user_organizations: Organization = Organization.objects.filter(users__in=[user]).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL ORGANIZATIONS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL ORGANIZATIONS'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_ORGANIZATIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_ORGANIZATIONS):
            messages.error(self.request, "You do not have permission to delete organizations.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for organization in user_organizations:
                organization.delete()
            messages.success(request, "All organizations associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting organizations: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')
