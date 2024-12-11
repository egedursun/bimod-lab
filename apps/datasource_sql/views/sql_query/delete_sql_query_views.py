#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_sql_query_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:41
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging

from django.contrib import messages

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.shortcuts import redirect
from django.views.generic import DeleteView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.datasource_sql.models import (
    CustomSQLQuery
)

from apps.user_permissions.utils import (
    PermissionNames
)

logger = logging.getLogger(__name__)


class SQLDatabaseView_QueryDelete(LoginRequiredMixin, DeleteView):
    model = CustomSQLQuery
    success_url = 'datasource_sql:list_queries'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - DELETE_CUSTOM_SQL_QUERIES
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_CUSTOM_SQL_QUERIES
        ):
            messages.error(self.request, "You do not have permission to delete custom SQL queries.")
            return redirect('datasource_sql:list_queries')
        ##############################

        try:
            self.object = self.get_object()
            self.object.delete()

        except Exception as e:
            logger.error(f"Error deleting SQL Query: {e}")
            messages.error(self.request, 'An error occurred while deleting SQL Query.')

            return redirect(self.success_url)

        logger.info(f"SQL Query {self.object.name} was deleted.")
        messages.success(request, f'SQL Query {self.object.name} was deleted successfully.')

        return redirect(self.success_url)
