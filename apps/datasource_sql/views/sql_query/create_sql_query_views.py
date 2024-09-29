#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: create_sql_query_views.py
#  Last Modified: 2024-09-28 00:53:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:49:30
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_sql.forms import CustomSQLQueryForm
from apps.datasource_sql.models import SQLDatabaseConnection
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


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
