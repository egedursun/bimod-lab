"""
This module contains views for managing SQL database connections and custom SQL queries within the Bimod.io platform.

The views include creating, updating, deleting, and listing SQL database connections and SQL queries. These views also handle form submissions, permission checks, and rendering templates for SQL-related operations. Access to these views is restricted to authenticated users, with additional permission checks for specific actions.
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, DeleteView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_sql.forms import SQLDatabaseConnectionForm, CustomSQLQueryForm
from apps.datasource_sql.models import DBMS_CHOICES, SQLDatabaseConnection, CustomSQLQuery
from apps.user_permissions.models import UserPermission, PermissionNames
from web_project import TemplateLayout


class CreateSQLDatabaseConnectionView(TemplateView, LoginRequiredMixin):
    """
    Handles the creation of new SQL database connections.

    This view displays a form for creating a new SQL database connection. Upon submission, it validates the input, checks user permissions, and saves the new connection to the database. If the user lacks the necessary permissions, an error message is displayed.

    Attributes:
        template_name (str): The template used to render the SQL database connection creation form.

    Methods:
        get_context_data(self, **kwargs): Adds additional context to the template, including the form for creating an SQL database connection and available assistants.
        post(self, request, *args, **kwargs): Handles form submission and SQL database connection creation, including permission checks and validation.
    """

    template_name = "datasource_sql/connections/create_sql_datasources.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        user_organizations = context_user.organizations.all()
        assistants = Assistant.objects.filter(organization__in=user_organizations)
        context['dbms_choices'] = DBMS_CHOICES
        context['form'] = SQLDatabaseConnectionForm()
        context['assistants'] = assistants
        return context

    def post(self, request, *args, **kwargs):
        form = SQLDatabaseConnectionForm(request.POST)
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - ADD_SQL_DATABASES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_SQL_DATABASES):
            messages.error(self.request, "You do not have permission to create SQL Data Sources.")
            return redirect('datasource_sql:list')
        ##############################

        if form.is_valid():
            form.save()
            messages.success(request, "SQL Data Source created successfully.")
            print('[CreateSQLDatabaseConnectionView.post] SQL Data Source created successfully.')
            return redirect('datasource_sql:create')
        else:
            messages.error(request, "Error creating SQL Data Source.")
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


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


class UpdateSQLDatabaseConnectionView(TemplateView, LoginRequiredMixin):
    """
    Handles updating an existing SQL database connection.

    This view allows users with the appropriate permissions to modify an SQL database connection's attributes. It also handles the form submission and validation for updating the connection.

    Methods:
        get_context_data(self, **kwargs): Retrieves the current SQL database connection details and adds them to the context, along with other relevant data such as available assistants and the form for updating the connection.
        post(self, request, *args, **kwargs): Handles form submission for updating the SQL database connection, including permission checks and validation.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        connection = SQLDatabaseConnection.objects.get(id=kwargs['pk'])
        user_organizations = context_user.organizations.all()
        assistants = Assistant.objects.filter(organization__in=user_organizations)
        context['dbms_choices'] = DBMS_CHOICES
        context['form'] = SQLDatabaseConnectionForm(instance=connection)
        context['assistants'] = assistants
        context['connection'] = connection
        return context

    def post(self, request, *args, **kwargs):
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - UPDATE_SQL_DATABASES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_SQL_DATABASES):
            messages.error(self.request, "You do not have permission to update SQL Data Sources.")
            return redirect('datasource_sql:list')
        ##############################

        connection = SQLDatabaseConnection.objects.get(id=kwargs['pk'], created_by_user=context_user)
        form = SQLDatabaseConnectionForm(request.POST, instance=connection)
        if form.is_valid():
            form.save()
            messages.success(request, "SQL Data Source updated successfully.")
            print('[UpdateSQLDatabaseConnectionView.post] SQL Data Source updated successfully.')
            return redirect('datasource_sql:list')
        else:
            messages.error(request, "Error updating SQL Data Source: " + str(form.errors))
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


class DeleteSQLDatabaseConnectionView(LoginRequiredMixin, DeleteView):
    """
    Handles the deletion of an SQL database connection.

    This view allows users with the appropriate permissions to delete an SQL database connection. It ensures that the user has the necessary permissions before performing the deletion.

    Methods:
        post(self, request, *args, **kwargs): Deletes the SQL database connection if the user has the required permissions.
    """

    model = SQLDatabaseConnection
    success_url = 'datasource_sql:list'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - DELETE_SQL_DATABASES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_SQL_DATABASES):
            messages.error(self.request, "You do not have permission to delete SQL Data Sources.")
            return redirect('datasource_sql:list')
        ##############################

        self.object = self.get_object()
        self.object.delete()
        messages.success(request, f'SQL Database Connection {self.object.name} was deleted successfully.')
        print(f'[DeleteSQLDatabaseConnectionView.post] SQL Database Connection {self.object.name} was deleted successfully.')
        return redirect(self.success_url)


class CreateSQLQueryView(TemplateView, LoginRequiredMixin):
    """
    Handles the creation of custom SQL queries.

    This view displays a form for creating a new SQL query. Upon submission, it validates the input, checks user permissions, and saves the new query to the database. If the user lacks the necessary permissions, an error message is displayed.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with available database connections and the form for creating an SQL query.
        post(self, request, *args, **kwargs): Handles form submission and SQL query creation, including permission checks and validation.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        user_organizations = context_user.organizations.all()
        database_connections = SQLDatabaseConnection.objects.filter(
            assistant__in=Assistant.objects.filter(organization__in=user_organizations)
        )
        context['database_connections'] = database_connections
        context['form'] = CustomSQLQueryForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CustomSQLQueryForm(request.POST)

        ##############################
        # PERMISSION CHECK FOR - ADD_CUSTOM_SQL_QUERIES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_CUSTOM_SQL_QUERIES):
            messages.error(self.request, "You do not have permission to create custom SQL queries.")
            return redirect('datasource_sql:list_queries')
        ##############################

        if form.is_valid():
            form.save()
            messages.success(request, "SQL Query created successfully.")
            print('[CreateSQLQueryView.post] SQL Query created successfully.')
            return redirect('datasource_sql:create_query')
        else:
            messages.error(request, "Error creating SQL Query.")
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


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


class DeleteSQLQueryView(LoginRequiredMixin, DeleteView):
    """
    Handles the deletion of a custom SQL query.

    This view allows users with the appropriate permissions to delete an SQL query. It ensures that the user has the necessary permissions before performing the deletion.

    Methods:
        post(self, request, *args, **kwargs): Deletes the SQL query if the user has the required permissions.
    """

    model = CustomSQLQuery
    success_url = 'datasource_sql:list_queries'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - DELETE_CUSTOM_SQL_QUERIES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_CUSTOM_SQL_QUERIES):
            messages.error(self.request, "You do not have permission to delete custom SQL queries.")
            return redirect('datasource_sql:list_queries')
        ##############################

        self.object = self.get_object()
        self.object.delete()
        messages.success(request, f'SQL Query {self.object.name} was deleted successfully.')
        return redirect(self.success_url)


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
            database_connection__assistant__in=Assistant.objects.filter(organization__in=context_user.organizations.all())
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
