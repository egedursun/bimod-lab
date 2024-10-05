#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: delete_all_custom_sql_queries_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:40
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.datasource_sql.models import CustomSQLQuery
from apps.user_permissions.utils import PermissionNames


class DeleteAllCustomSQLQueriesView(View, LoginRequiredMixin):
    """
    Handles the deletion of all custom SQL queries associated with the user account.
    """

    def post(self, request, *args, **kwargs):
        user = request.user
        user_custom_sql_queries = CustomSQLQuery.objects.filter(
            database_connection__assistant__organization__users__in=[user]
        ).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL CUSTOM SQL QUERIES':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL CUSTOM SQL QUERIES'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_CUSTOM_SQL_QUERIES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_CUSTOM_SQL_QUERIES):
            messages.error(self.request, "You do not have permission to delete custom SQL queries.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for custom_sql_query in user_custom_sql_queries:
                custom_sql_query.delete()
            messages.success(request, "All custom SQL queries associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting custom SQL queries: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')
