from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.datasource_codebase.models import CodeBaseRepository
from apps.user_permissions.utils import PermissionNames


class DeleteAllRepositoriesView(View, LoginRequiredMixin):
    """
    Handles the deletion of all repositories associated with the user account.
    """

    def post(self, request, *args, **kwargs):
        user = request.user
        user_repositories = CodeBaseRepository.objects.filter(
            knowledge_base__assistant__organization__users__in=[user]
        ).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL REPOSITORIES':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL REPOSITORIES'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_CODE_REPOSITORY
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_CODE_REPOSITORY):
            messages.error(self.request, "You do not have permission to delete code repositories.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for repository in user_repositories:
                repository.delete()
            messages.success(request, "All repositories associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting repositories: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')
