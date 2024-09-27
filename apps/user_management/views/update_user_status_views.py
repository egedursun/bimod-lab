from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.user_permissions.models import PermissionNames


@method_decorator(require_POST, name='dispatch')
class UpdateUserStatusView(LoginRequiredMixin, TemplateView):
    """
    View to update the active status of a user.

    This view allows administrators to activate or deactivate a user. The user's active status in all associated permissions is also updated accordingly.

    Methods:
        post(self, request, *args, **kwargs): Handles the logic to update the user's active status.
    """

    def post(self, request, *args, **kwargs):
        context_user = self.request.user
        user_id = request.POST.get('user_id')
        is_active = request.POST.get('is_active') == 'true'

        ##############################
        # PERMISSION CHECK FOR - UPDATE_USERS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_USERS):
            messages.error(self.request, "You do not have permission to update/modify user accounts.")
            return redirect('user_management:list')
        ##############################

        try:
            user = User.objects.get(id=user_id)
            user.profile.is_active = is_active
            user.profile.save()
            return redirect('user_management:list')
        except Exception as e:
            print(f'[UpdateUserStatusView.post] Error updating user status: {str(e)}')
            messages.error(request, f'Error updating user status')
            return redirect('user_management:list')
