from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_ml_models.forms import DataSourceMLModelConnectionForm
from apps.datasource_ml_models.models import DataSourceMLModelConnection
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DataSourceMLModelConnectionUpdateView(LoginRequiredMixin, TemplateView):
    """
    Handles updating an existing machine learning model connection.

    This view allows users with the appropriate permissions to modify an ML model connection's attributes. It also handles the form submission and validation for updating the connection.

    Methods:
        get_context_data(self, **kwargs): Retrieves the current ML model connection details and adds them to the context, along with other relevant data such as available assistants and the form for updating the connection.
        post(self, request, *args, **kwargs): Handles form submission for updating the ML model connection, including permission checks and validation.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        connection = DataSourceMLModelConnection.objects.get(id=kwargs['pk'])
        user_organizations = context_user.organizations.all()
        assistants = Assistant.objects.filter(organization__in=user_organizations)
        context['form'] = DataSourceMLModelConnectionForm(instance=connection)
        context['assistants'] = assistants
        context['connection'] = connection
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_ML_MODEL_CONNECTIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_ML_MODEL_CONNECTIONS):
            messages.error(self.request, "You do not have permission to update ML Model Connections.")
            return redirect('datasource_ml_models:list')
        ##############################

        connection = DataSourceMLModelConnection.objects.get(id=kwargs['pk'])
        form = DataSourceMLModelConnectionForm(request.POST, instance=connection)
        if form.is_valid():
            form.save()
            messages.success(request, "ML Model Connection updated successfully.")
            print('[DataSourceMLModelConnectionUpdateView.post] ML Model Connection updated successfully.')
            return redirect('datasource_ml_models:list')
        else:
            messages.error(request, "Error updating ML Model Connection: " + str(form.errors))
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)
