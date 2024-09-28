from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_sql.models import CustomSQLQuery
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class ListSQLQueriesView(TemplateView, LoginRequiredMixin):
    """
    Displays a list of custom SQL queries associated with the user's SQL database connections.

    This view retrieves all custom SQL queries within the user's SQL database connections, organized by organization and assistant, and displays them in a structured list.

    Methods:
        get_context_data(self, **kwargs): Retrieves the SQL queries for the user's connections and adds them to the context, including organization and assistant details.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_CUSTOM_SQL_QUERIES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_CUSTOM_SQL_QUERIES):
            messages.error(self.request, "You do not have permission to list custom SQL queries.")
            return context
        ##############################

        context_user = self.request.user
        queries = CustomSQLQuery.objects.filter(
            database_connection__assistant__in=Assistant.objects.filter(
                organization__in=context_user.organizations.all())
        ).select_related('database_connection__assistant', 'database_connection__assistant__organization')

        queries_by_organization = {}
        for query in queries:
            organization = query.database_connection.assistant.organization
            assistant = query.database_connection.assistant

            if organization not in queries_by_organization:
                queries_by_organization[organization] = {}
            if assistant not in queries_by_organization[organization]:
                queries_by_organization[organization][assistant] = []
            queries_by_organization[organization][assistant].append(query)
        context['queries_by_organization'] = queries_by_organization
        return context
