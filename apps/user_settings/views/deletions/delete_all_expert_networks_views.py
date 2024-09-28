from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.leanmod.models import ExpertNetwork
from apps.user_permissions.utils import PermissionNames


class DeleteAllExpertNetworksView(View, LoginRequiredMixin):
    """
    Handles the deletion of expert networks associated with the user account.
    """

    def post(self, request, *args, **kwargs):
        user = request.user
        user_assistants = ExpertNetwork.objects.filter(organization__users__in=[user]).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL EXPERT NETWORKS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL EXPERT NETWORKS'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_EXPERT_NETWORKS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_EXPERT_NETWORKS):
            messages.error(self.request, "You do not have permission to delete expert networks.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for assistant in user_assistants:
                assistant.delete()
            messages.success(request, "All expert networks associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting expert networks: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')
