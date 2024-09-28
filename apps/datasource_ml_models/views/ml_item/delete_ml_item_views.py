from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DataSourceMLModelItemDeleteView(LoginRequiredMixin, TemplateView):
    """
    Handles the deletion of a specific machine learning model item.

    This view allows users with the appropriate permissions to delete an ML model item.

    Methods:
        get_context_data(self, **kwargs): Prepares the context for rendering the confirmation of the deletion.
        post(self, request, *args, **kwargs): Deletes the ML model item if the user has the required permissions.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - DELETE_ML_MODEL_FILES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_ML_MODEL_FILES):
            messages.error(self.request, "You do not have permission to delete ML Model files.")
            return redirect('datasource_ml_models:item_list')
        ##############################

        print('[DataSourceMLModelItemDeleteView.post] Deleting ML Model Item')
        return self.render_to_response(self.get_context_data(**kwargs))
