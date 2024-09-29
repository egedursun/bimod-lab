#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: delete_sql_database_views.py
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
from django.views.generic import DeleteView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.datasource_sql.models import SQLDatabaseConnection
from apps.user_permissions.utils import PermissionNames


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
        print(
            f'[DeleteSQLDatabaseConnectionView.post] SQL Database Connection {self.object.name} was deleted successfully.')
        return redirect(self.success_url)
