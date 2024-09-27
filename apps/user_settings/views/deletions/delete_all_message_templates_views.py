from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.message_templates.models import MessageTemplate
from apps.user_permissions.models import PermissionNames


class DeleteAllMessageTemplatesView(View, LoginRequiredMixin):
    """
    Handles the deletion of all message templates associated with the user account.
    """

    def post(self, request, *args, **kwargs):
        user = request.user
        user_message_templates = MessageTemplate.objects.filter(user=user).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL MESSAGE TEMPLATES':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL MESSAGE TEMPLATES'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - REMOVE_TEMPLATE_MESSAGES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.REMOVE_TEMPLATE_MESSAGES):
            messages.error(self.request, "You do not have permission to delete message templates.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for message_template in user_message_templates:
                message_template.delete()
            messages.success(request, "All message templates associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting message templates: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')
