from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DeleteView

from apps.assistants.models import Assistant
from apps.datasource_sql.forms import SQLDatabaseConnectionForm
from apps.datasource_sql.models import DBMS_CHOICES, SQLDatabaseConnection
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
        context['sql_connections'] = SQLDatabaseConnection.objects.filter(
            assistant__in=Assistant.objects.filter(organization__in=context_user.organizations.all())
        )
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
        self.object.delete()
        messages.success(request, f'SQL Database Connection {self.object.name} was deleted successfully.')
        return redirect(self.success_url)


##################################################


class CreateSQLQueryView(TemplateView, LoginRequiredMixin):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context


class UpdateSQLQueryView(TemplateView, LoginRequiredMixin):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context


class DeleteSQLQueryView(DeleteView, LoginRequiredMixin):
    pass
