from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_ml_models.models import DataSourceMLModelConnection
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DataSourceMLModelConnectionListView(LoginRequiredMixin, TemplateView):
    """
    Displays a list of machine learning model connections associated with the user's organizations and assistants.

    This view retrieves all ML model connections organized by organization and assistant, and displays them in a structured list.

    Attributes:
        template_name (str): The template used to render the ML model connection list.

    Methods:
        get_context_data(self, **kwargs): Retrieves the ML model connections organized by organization and assistant, and adds them to the context.
    """

    template_name = 'datasource_ml_models/base/list_datasource_ml_models.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_ML_MODEL_CONNECTIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_ML_MODEL_CONNECTIONS):
            messages.error(self.request, "You do not have permission to list ML Model Connections.")
            return context
        ##############################

        context_user = self.request.user
        connections = DataSourceMLModelConnection.objects.filter(
            assistant__in=Assistant.objects.filter(organization__in=context_user.organizations.all())
        ).select_related('assistant__organization')

        connections_by_organization = {}
        for connection in connections:
            organization = connection.assistant.organization
            assistant = connection.assistant

            if organization not in connections_by_organization:
                connections_by_organization[organization] = {}
            if assistant not in connections_by_organization[organization]:
                connections_by_organization[organization][assistant] = []
            connections_by_organization[organization][assistant].append(connection)
        context['connections_by_organization'] = connections_by_organization
        return context
