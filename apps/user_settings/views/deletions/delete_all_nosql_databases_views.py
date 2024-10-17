#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_all_nosql_databases_views.py
#  Last Modified: 2024-10-17 12:31:51
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 12:32:28
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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.datasource_nosql.models import NoSQLDatabaseConnection
from apps.user_permissions.utils import PermissionNames


logger = logging.getLogger(__name__)


class SettingsView_DeleteAllNoSQLDBs(View, LoginRequiredMixin):
    def post(self, request, *args, **kwargs):
        user = request.user
        user_nosql_databases = NoSQLDatabaseConnection.objects.filter(assistant__organization__users__in=[user]).all()
        confirmation_field = request.POST.get('confirmation', None)
        if confirmation_field != 'CONFIRM DELETING ALL NOSQL DATABASES':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL NOSQL DATABASES'.")
            logger.error(f"Invalid confirmation field: {confirmation_field}")
            return redirect('user_settings:settings')

        ##############################
        # PERMISSION CHECK FOR - DELETE_NOSQL_DATABASES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_NOSQL_DATABASES):
            messages.error(self.request, "You do not have permission to delete NoSQL databases.")
            return redirect('user_settings:settings')
        ##############################

        try:
            for nosql_database in user_nosql_databases:
                nosql_database.delete()
            messages.success(request, "All NoSQL databases associated with your account have been deleted.")
            logger.info(f"All NoSQL databases associated with User: {user.id} have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting NoSQL databases: {e}")
            logger.error(f"Error deleting NoSQL databases: {e}")
        return redirect('user_settings:settings')
