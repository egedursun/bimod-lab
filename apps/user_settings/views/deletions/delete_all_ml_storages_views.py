from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.datasource_ml_models.models import DataSourceMLModelConnection
from apps.user_permissions.models import PermissionNames


class DeleteAllMLModelStoragesView(View, LoginRequiredMixin):
    """
    Handles the deletion of all ML model storages associated with the user account.
    """

    def post(self, request, *args, **kwargs):
        user = request.user
        user_ml_model_storages = DataSourceMLModelConnection.objects.filter(
            assistant__organization__users__in=[user]).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL ML MODEL STORAGES':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL ML MODEL STORAGES'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_ML_MODEL_CONNECTIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_ML_MODEL_CONNECTIONS):
            messages.error(self.request, "You do not have permission to delete ML model storages.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for ml_model_storage in user_ml_model_storages:
                ml_model_storage.delete()
            messages.success(request, "All ML model storages associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting ML model storages: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')
