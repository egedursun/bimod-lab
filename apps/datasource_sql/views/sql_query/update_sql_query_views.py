from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_sql.forms import CustomSQLQueryForm
from apps.datasource_sql.models import CustomSQLQuery, SQLDatabaseConnection
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class UpdateSQLQueryView(TemplateView, LoginRequiredMixin):
    """
    Handles updating an existing custom SQL query.

    This view allows users with the appropriate permissions to modify an SQL query's attributes. It also handles the form submission and validation for updating the query.

    Methods:
        get_context_data(self, **kwargs): Retrieves the current SQL query details and adds them to the context, along with other relevant data such as available database connections and the form for updating the query.
        post(self, request, *args, **kwargs): Handles form submission for updating the SQL query, including permission checks and validation.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        query = get_object_or_404(CustomSQLQuery, id=kwargs['pk'])
        user_organizations = context_user.organizations.all()
        database_connections = SQLDatabaseConnection.objects.filter(
            assistant__in=Assistant.objects.filter(organization__in=user_organizations)
        )
        context['database_connections'] = database_connections
        context['form'] = CustomSQLQueryForm(instance=query)
        context['query'] = query
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_CUSTOM_SQL_QUERIES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_CUSTOM_SQL_QUERIES):
            messages.error(self.request, "You do not have permission to update custom SQL queries.")
            return redirect('datasource_sql:list_queries')
        ##############################

        query = get_object_or_404(CustomSQLQuery, id=kwargs['pk'])
        form = CustomSQLQueryForm(request.POST, instance=query)
        if form.is_valid():
            form.save()
            messages.success(request, "SQL Query updated successfully.")
            print('[UpdateSQLQueryView.post] SQL Query updated successfully.')
            return redirect('datasource_sql:list_queries')
        else:
            messages.error(request, "Error updating SQL Query: " + str(form.errors))
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)
