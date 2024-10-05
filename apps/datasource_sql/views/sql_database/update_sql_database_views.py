#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: update_sql_database_views.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:38
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: update_sql_database_views.py
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
from apps.datasource_sql.forms import SQLDatabaseConnectionForm
from apps.datasource_sql.models import SQLDatabaseConnection
from apps.datasource_sql.utils import DBMS_CHOICES
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


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
