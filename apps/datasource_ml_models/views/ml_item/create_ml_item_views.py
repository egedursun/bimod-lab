from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_ml_models.forms import DataSourceMLModelItemForm
from apps.datasource_ml_models.models import DataSourceMLModelConnection
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DataSourceMLModelItemCreateView(LoginRequiredMixin, TemplateView):
    """
    Handles uploading machine learning model files to a selected ML model connection.

    This view displays a form for selecting an ML model connection and uploading ML model files to it. Upon form submission, it validates the input, reads the file contents, and saves the ML model items to the database. If the user lacks the necessary permissions, an error message is displayed.

    Attributes:
        template_name (str): The template used to render the ML model item creation form.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with the available ML model connections and the form for uploading ML model items.
        post(self, request, *args, **kwargs): Handles the ML model file upload process, including validation and saving the ML model items.
    """

    template_name = 'datasource_ml_models/models/create_datasource_ml_model_item.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        user_organizations = context_user.organizations.all()
        user_assistants = Assistant.objects.filter(organization__in=user_organizations)
        ml_model_connections = DataSourceMLModelConnection.objects.filter(
            assistant__in=user_assistants
        ).all()
        context['ml_model_connections'] = ml_model_connections
        context['form'] = DataSourceMLModelItemForm()
        return context

    def post(self, request, *args, **kwargs):
        form = DataSourceMLModelItemForm(request.POST, request.FILES)

        ##############################
        # PERMISSION CHECK FOR - ADD_ML_MODEL_FILES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_ML_MODEL_FILES):
            messages.error(self.request, "You do not have permission to add ML Model files.")
            return redirect('datasource_ml_models:item_list')
        ##############################

        if form.is_valid():
            ml_model_item = form.save(commit=False)
            uploaded_file = request.FILES['file']
            ml_model_item.file_bytes = uploaded_file.read()
            ml_model_item.ml_model_size = uploaded_file.size
            ml_model_item.created_by_user = request.user
            ml_model_item.save()
            print('[DataSourceMLModelItemCreateView.post] ML Model Item uploaded successfully.')
            messages.success(request, 'ML Model Item uploaded successfully.')
            return redirect('datasource_ml_models:item_list')
        else:
            messages.error(request, 'There was an error uploading the ML Model Item.')
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)
