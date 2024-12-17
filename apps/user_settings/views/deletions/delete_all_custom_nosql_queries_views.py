#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_all_custom_nosql_queries_views.py
#  Last Modified: 2024-10-17 12:34:14
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 12:34:30
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
from django.views import View

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.datasource_nosql.models import (
    CustomNoSQLQuery
)

from apps.user_permissions.utils import (
    PermissionNames
)

logger = logging.getLogger(__name__)


class SettingsView_DeleteAllNoSQLQueries(View, LoginRequiredMixin):

    def post(self, request, *args, **kwargs):
        user = request.user

        user_custom_nosql_queries = CustomNoSQLQuery.objects.filter(
            database_connection__assistant__organization__users__in=[user]
        ).all()

        confirmation_field = request.POST.get('confirmation', None)

        if confirmation_field != 'CONFIRM DELETING ALL CUSTOM NOSQL QUERIES':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL CUSTOM NOSQL QUERIES'.")
            logger.error(f"Invalid confirmation field: {confirmation_field}")

            return redirect('user_settings:settings')

        ##############################
        # PERMISSION CHECK FOR - DELETE_CUSTOM_NOSQL_QUERIES
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_CUSTOM_NOSQL_QUERIES
        ):
            messages.error(self.request, "You do not have permission to delete custom NoSQL queries.")

            return redirect('user_settings:settings')
        ##############################

        try:
            for custom_nosql_query in user_custom_nosql_queries:
                custom_nosql_query.delete()

            messages.success(request, "All custom NoSQL queries associated with your account have been deleted.")
            logger.info(f"All custom NoSQL queries associated with User: {user.id} have been deleted.")

        except Exception as e:
            messages.error(request, f"Error deleting custom NoSQL queries: {e}")
            logger.error(f"Error deleting custom NoSQL queries: {e}")

        return redirect('user_settings:settings')
