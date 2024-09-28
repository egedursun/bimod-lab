from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.leanmod.models import LeanAssistant
from apps.user_permissions.utils import PermissionNames


class DeleteAllLeanAssistantsView(View, LoginRequiredMixin):
    """
    Handles the deletion of all lean assistants associated with the user account.
    """

    def post(self, request, *args, **kwargs):
        user = request.user
        user_assistants = LeanAssistant.objects.filter(organization__users__in=[user]).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL LEAN ASSISTANTS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL LEAN ASSISTANTS'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_LEAN_ASSISTANT
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_LEAN_ASSISTANT):
            messages.error(self.request, "You do not have permission to delete LeanMod assistants.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for assistant in user_assistants:
                assistant.delete()
            messages.success(request, "All lean assistants associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting lean assistants: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')
