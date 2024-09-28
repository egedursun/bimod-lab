from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_sql.models import SQLDatabaseConnection
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class ListSQLDatabaseConnectionsView(TemplateView, LoginRequiredMixin):
    """
    Displays a list of SQL database connections associated with the user's organizations and assistants.

    This view retrieves all SQL database connections organized by organization and assistant and displays them in a structured list.

    Methods:
        get_context_data(self, **kwargs): Retrieves the SQL database connections organized by organization and assistant, and adds them to the context.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_SQL_DATABASES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_SQL_DATABASES):
            messages.error(self.request, "You do not have permission to list SQL Data Sources.")
            return context
        ##############################

        context_user = self.request.user
        connections = SQLDatabaseConnection.objects.filter(
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
