from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, DeleteView

from apps.assistants.models import Assistant
from apps.datasource_nosql.forms import NoSQLDatabaseConnectionForm, CustomNoSQLQueryForm
from apps.datasource_nosql.models import NoSQLDatabaseConnection, DBMS_CHOICES, CustomNoSQLQuery
from apps.user_permissions.models import PermissionNames, UserPermission
from web_project import TemplateLayout


# Create your views here.

class CreateNoSQLDataSourcesView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        user_organizations = context_user.organizations.all()
        assistants = Assistant.objects.filter(organization__in=user_organizations)
        context['dbms_choices'] = DBMS_CHOICES
        context['form'] = NoSQLDatabaseConnectionForm()
        context['assistants'] = assistants
        return context

    def post(self, request, *args, **kwargs):
        form = NoSQLDatabaseConnectionForm(request.POST)
        context_user = self.request.user

        # Permission check for NoSQL data source creation
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.ADD_NOSQL_DATABASES not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {
                "Permission Error": "You do not have permission to create NoSQL Data Sources."
            }
            return self.render_to_response(context)

        if form.is_valid():
            form.save()
            messages.success(request, "NoSQL Data Source created successfully.")
            return redirect('datasource_nosql:list')
        else:
            messages.error(request, "Error creating NoSQL Data Source: " + str(form.errors))
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


class UpdateNoSQLDataSourceView(LoginRequiredMixin, TemplateView):
    template_name = "datasource_nosql/update_nosql_datasource.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        connection = NoSQLDatabaseConnection.objects.get(id=kwargs['pk'])
        user_organizations = context_user.organizations.all()
        assistants = Assistant.objects.filter(organization__in=user_organizations)
        context['dbms_choices'] = DBMS_CHOICES
        context['form'] = NoSQLDatabaseConnectionForm(instance=connection)
        context['assistants'] = assistants
        context['connection'] = connection
        return context

    def post(self, request, *args, **kwargs):
        context_user = self.request.user

        # Permission check for NoSQL data source update
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.UPDATE_NOSQL_DATABASES not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {
                "Permission Error": "You do not have permission to update NoSQL Data Sources."
            }
            return self.render_to_response(context)

        connection = NoSQLDatabaseConnection.objects.get(id=kwargs['pk'])
        form = NoSQLDatabaseConnectionForm(request.POST, instance=connection)
        if form.is_valid():
            form.save()
            messages.success(request, "NoSQL Data Source updated successfully.")
            return redirect('datasource_nosql:list')
        else:
            messages.error(request, "Error updating NoSQL Data Source: " + str(form.errors))
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


class DeleteNoSQLDataSourceView(LoginRequiredMixin, DeleteView):
    model = NoSQLDatabaseConnection
    success_url = 'datasource_nosql:list'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context_user = request.user

        # Permission check for NoSQL data source delete
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.DELETE_NOSQL_DATABASES not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {
                "Permission Error": "You do not have permission to delete NoSQL Data Sources."
            }
            return self.render_to_response(context)

        self.object.delete()
        messages.success(request, f'NoSQL Database Connection {self.object.name} was deleted successfully.')
        return redirect(self.success_url)


class ListNoSQLDataSourcesView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        connections = NoSQLDatabaseConnection.objects.filter(
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


####################################################################################################


class CreateNoSQLQueryView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        user_organizations = context_user.organizations.all()
        database_connections = NoSQLDatabaseConnection.objects.filter(
            assistant__in=Assistant.objects.filter(organization__in=user_organizations)
        )
        context['database_connections'] = database_connections
        context['form'] = CustomNoSQLQueryForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CustomNoSQLQueryForm(request.POST)
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - NOSQL QUERY CREATION
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.ADD_NOSQL_DATABASES not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {
                "Permission Error": "You do not have permission to create NoSQL Queries."
            }
            return self.render_to_response(context)
        ##############################

        if form.is_valid():
            form.save()
            messages.success(request, "NoSQL Query created successfully.")
            return redirect('datasource_nosql:list_queries')
        else:
            messages.error(request, "Error creating NoSQL Query: " + str(form.errors))
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


class UpdateNoSQLQueryView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        query = get_object_or_404(CustomNoSQLQuery, id=kwargs['pk'])
        user_organizations = context_user.organizations.all()
        database_connections = NoSQLDatabaseConnection.objects.filter(
            assistant__in=Assistant.objects.filter(organization__in=user_organizations)
        )
        context['database_connections'] = database_connections
        context['form'] = CustomNoSQLQueryForm(instance=query)
        context['query'] = query
        return context

    def post(self, request, *args, **kwargs):
        context_user = self.request.user
        query = get_object_or_404(CustomNoSQLQuery, id=kwargs['pk'])

        ##############################
        # PERMISSION CHECK FOR - NoSQL QUERY UPDATE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.UPDATE_NOSQL_DATABASES not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {
                "Permission Error": "You do not have permission to update NoSQL Queries."
            }
            return self.render_to_response(context)
        ##############################

        form = CustomNoSQLQueryForm(request.POST, instance=query)
        if form.is_valid():
            form.save()
            messages.success(request, "NoSQL Query updated successfully.")
            return redirect('datasource_nosql:list_queries')
        else:
            messages.error(request, "Error updating NoSQL Query: " + str(form.errors))
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


class DeleteNoSQLQueryView(LoginRequiredMixin, DeleteView):
    model = CustomNoSQLQuery
    success_url = 'datasource_nosql:list_queries'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context_user = request.user

        ##############################
        # PERMISSION CHECK FOR - NoSQL QUERY DELETE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.DELETE_NOSQL_DATABASES not in user_permissions:
            messages.error(request, "You do not have permission to delete NoSQL Queries.")
            return redirect(self.success_url)
        ##############################

        self.object.delete()
        messages.success(request, f'NoSQL Query {self.object.name} was deleted successfully.')
        return redirect(self.success_url)


class ListNoSQLQueriesView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        queries = CustomNoSQLQuery.objects.filter(
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
