from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.datasource_media_storages.models import DataSourceMediaStorageConnection
from apps.user_permissions.utils import PermissionNames


class DeleteAllMediaStoragesView(View, LoginRequiredMixin):
    """
    Handles the deletion of all media storages associated with the user account.
    """

    def post(self, request, *args, **kwargs):
        user = request.user
        user_media_storages = DataSourceMediaStorageConnection.objects.filter(
            assistant__organization__users__in=[user]).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL MEDIA STORAGES':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL MEDIA STORAGES'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_MEDIA_STORAGES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_MEDIA_STORAGES):
            messages.error(self.request, "You do not have permission to delete media storages.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for media_storage in user_media_storages:
                media_storage.delete()
            messages.success(request, "All media storages associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting media storages: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')
