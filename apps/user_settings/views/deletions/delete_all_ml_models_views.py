from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.datasource_ml_models.models import DataSourceMLModelItem
from apps.user_permissions.utils import PermissionNames


class DeleteAllMLModelsView(View, LoginRequiredMixin):
    """
    Handles the deletion of all ML models associated with the user account.
    """

    def post(self, request, *args, **kwargs):
        user = request.user
        user_ml_models = DataSourceMLModelItem.objects.filter(
            ml_model_base__assistant__organization__users__in=[user]
        ).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL ML MODELS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL ML MODELS'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_ML_MODEL_FILES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_ML_MODEL_FILES):
            messages.error(self.request, "You do not have permission to delete ML model files.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for ml_model in user_ml_models:
                ml_model.delete()
            messages.success(request, "All ML models associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting ML models: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')
