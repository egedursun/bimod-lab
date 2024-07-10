from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, DeleteView

from apps.assistants.models import Assistant
from apps.datasource_sql.forms import SQLDatabaseConnectionForm, CustomSQLQueryForm
from apps.datasource_sql.models import DBMS_CHOICES, SQLDatabaseConnection, CustomSQLQuery
from apps.user_permissions.models import UserPermission, PermissionNames
from web_project import TemplateLayout


# Create your views here.


class CreateSQLDatabaseConnectionView(TemplateView, LoginRequiredMixin):
    template_name = "datasource_sql/create_sql_datasources.html"

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
        # PERMISSION CHECK FOR - SQL DATA SOURCE CREATION
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.ADD_SQL_DATABASES not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {
                "Permission Error": "You do not have permission to create SQL Data Sources."
            }
            return self.render_to_response(context)
        ##############################

        if form.is_valid():
            form.save()
            messages.success(request, "SQL Data Source created successfully.")
            return redirect('datasource_sql:create')
        else:
            messages.error(request, "Error creating SQL Data Source.")
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


class ListSQLDatabaseConnectionsView(TemplateView, LoginRequiredMixin):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
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

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        connection = SQLDatabaseConnection.objects.get(id=kwargs['pk'], created_by_user=context_user)
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
        # PERMISSION CHECK FOR - SQL DATA SOURCE UPDATE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.UPDATE_SQL_DATABASES not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {
                "Permission Error": "You do not have permission to update SQL Data Sources."
            }
            return self.render_to_response(context)
        ##############################

        connection = SQLDatabaseConnection.objects.get(id=kwargs['pk'], created_by_user=context_user)
        form = SQLDatabaseConnectionForm(request.POST, instance=connection)
        if form.is_valid():
            form.save()
            messages.success(request, "SQL Data Source updated successfully.")
            return redirect('datasource_sql:list')
        else:
            messages.error(request, "Error updating SQL Data Source: " + str(form.errors))
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


class DeleteSQLDatabaseConnectionView(LoginRequiredMixin, DeleteView):
    model = SQLDatabaseConnection
    success_url = 'datasource_sql:list'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context_user = request.user

        ##############################
        # PERMISSION CHECK FOR - SQL DATA SOURCE DELETE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.DELETE_SQL_DATABASES not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {
                "Permission Error": "You do not have permission to delete SQL Data Sources."
            }
            return self.render_to_response(context)
        ##############################

        self.object.delete()
        messages.success(request, f'SQL Database Connection {self.object.name} was deleted successfully.')
        return redirect(self.success_url)


##################################################


class CreateSQLQueryView(TemplateView, LoginRequiredMixin):

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
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - SQL QUERY CREATION
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.ADD_SQL_DATABASES not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {
                "Permission Error": "You do not have permission to create SQL Queries."
            }
            return self.render_to_response(context)
        ##############################

        if form.is_valid():
            form.save()
            messages.success(request, "SQL Query created successfully.")
            return redirect('datasource_sql:create_query')
        else:
            messages.error(request, "Error creating SQL Query.")
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


class UpdateSQLQueryView(TemplateView, LoginRequiredMixin):

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
        context_user = self.request.user
        query = get_object_or_404(CustomSQLQuery, id=kwargs['pk'])

        ##############################
        # PERMISSION CHECK FOR - SQL QUERY UPDATE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.UPDATE_SQL_DATABASES not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {
                "Permission Error": "You do not have permission to update SQL Queries."
            }
            return self.render_to_response(context)
        ##############################

        form = CustomSQLQueryForm(request.POST, instance=query)
        if form.is_valid():
            form.save()
            messages.success(request, "SQL Query updated successfully.")
            return redirect('datasource_sql:list_queries')
        else:
            messages.error(request, "Error updating SQL Query: " + str(form.errors))
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


class DeleteSQLQueryView(LoginRequiredMixin, DeleteView):
    model = CustomSQLQuery
    success_url = 'datasource_sql:list_queries'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context_user = request.user

        ##############################
        # PERMISSION CHECK FOR - SQL QUERY DELETE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.DELETE_SQL_DATABASES not in user_permissions:
            messages.error(request, "You do not have permission to delete SQL Queries.")
            return redirect(self.success_url)
        ##############################

        self.object.delete()
        messages.success(request, f'SQL Query {self.object.name} was deleted successfully.')
        return redirect(self.success_url)


class ListSQLQueriesView(TemplateView, LoginRequiredMixin):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
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
