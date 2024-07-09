from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DeleteView

from apps.assistants.models import Assistant
from apps.datasource_sql.forms import SQLDatabaseConnectionForm
from apps.datasource_sql.models import DBMS_CHOICES
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
        return context


class UpdateSQLDatabaseConnectionView(TemplateView, LoginRequiredMixin):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context


class DeleteSQLDatabaseConnectionView(DeleteView, LoginRequiredMixin):
    pass


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
