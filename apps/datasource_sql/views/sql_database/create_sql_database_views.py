from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_sql.forms import SQLDatabaseConnectionForm
from apps.datasource_sql.utils import DBMS_CHOICES
from apps.user_permissions.models import PermissionNames
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
