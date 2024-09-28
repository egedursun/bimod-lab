from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import DeleteView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.datasource_sql.models import CustomSQLQuery
from apps.user_permissions.utils import PermissionNames


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
