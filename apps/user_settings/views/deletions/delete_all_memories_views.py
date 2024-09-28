from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.memories.models import AssistantMemory
from apps.user_permissions.utils import PermissionNames


class DeleteAllMemoriesView(View, LoginRequiredMixin):
    """
    Handles the deletion of all memories associated with the user account.
    """

    def post(self, request, *args, **kwargs):
        user = request.user
        user_memories = AssistantMemory.objects.filter(user=user).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL MEMORIES':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL MEMORIES'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_ASSISTANT_MEMORIES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_ASSISTANT_MEMORIES):
            messages.error(self.request, "You do not have permission to delete assistant memories.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for memory in user_memories:
                memory.delete()
            messages.success(request, "All memories associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting memories: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')
