from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.starred_messages.models import StarredMessage
from apps.user_permissions.models import PermissionNames


class DeleteAllStarredMessagesView(View, LoginRequiredMixin):
    """
    Handles the deletion of all starred messages associated with the user account.
    """

    def post(self, request, *args, **kwargs):
        user = request.user
        user_starred_messages = StarredMessage.objects.filter(user=user).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL STARRED MESSAGES':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL STARRED MESSAGES'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - REMOVE_STARRED_MESSAGES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.REMOVE_STARRED_MESSAGES):
            messages.error(self.request, "You do not have permission to remove starred messages.")
            return redirect('user_settings:settings')
        ##############################

        # [2] Delete ALL items in the queryset
        try:
            for starred_message in user_starred_messages:
                starred_message.delete()
            messages.success(request, "All starred messages associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting starred messages: {e}")

        # [3] Redirect back to settings page
        return redirect('user_settings:settings')
