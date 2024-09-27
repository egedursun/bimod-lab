from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.datasource_media_storages.models import DataSourceMediaStorageItem
from apps.user_permissions.models import PermissionNames


class DeleteAllMultimediaFilesView(View, LoginRequiredMixin):
    """
    Handles the deletion of all multimedia files associated with the user account.
    """

    def post(self, request, *args, **kwargs):
        user = request.user
        user_multimedia_files = DataSourceMediaStorageItem.objects.filter(
            storage_base__assistant__organization__users__in=[user]
        ).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL MULTIMEDIA FILES':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL MULTIMEDIA FILES'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_STORAGE_FILES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_STORAGE_FILES):
            messages.error(self.request, "You do not have permission to delete multimedia files.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for multimedia_file in user_multimedia_files:
                multimedia_file.delete()
            messages.success(request, "All multimedia files associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting multimedia files: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')
