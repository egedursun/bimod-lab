#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_all_hadron_execution_logs_views.py
#  Last Modified: 2024-10-18 21:54:59
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-18 21:55:35
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

from apps.hadron_prime.models import (
    HadronNodeExecutionLog
)

from apps.organization.models import Organization

from apps.user_permissions.utils import (
    PermissionNames
)

logger = logging.getLogger(__name__)


class SettingsView_DeleteAllHadronNodeExecutionLogs(View, LoginRequiredMixin):

    def post(self, request, *args, **kwargs):
        user = request.user

        user_orgs = Organization.objects.filter(
            users__in=[user]
        )

        hadron_node_exec_logs = HadronNodeExecutionLog.objects.filter(
            node__system__organization__in=user_orgs
        )

        confirmation_field = request.POST.get('confirmation', None)

        if confirmation_field != 'CONFIRM DELETING ALL HADRON NODE EXECUTION LOGS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL HADRON NODE EXECUTION LOGS'.")
            logger.error(f"Invalid confirmation field: {confirmation_field}")

            return redirect('user_settings:settings')

        ##############################
        # PERMISSION CHECK FOR - DELETE_HADRON_NODE_EXECUTION_LOGS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_HADRON_NODE_EXECUTION_LOGS
        ):
            messages.error(self.request, "You do not have permission to delete hadron node execution nodes.")

            return redirect('user_settings:settings')
        ##############################

        try:
            for hadron_node_exec_log in hadron_node_exec_logs:
                hadron_node_exec_log.delete()

            logger.info(f"All hadron node execution logs associated with User: {user.id} have been deleted.")
            messages.success(request, "All hadron node execution logs associated with your account have been deleted.")

        except Exception as e:
            logger.error(f"Error deleting hadron node execution logs: {e}")
            messages.error(request, f"Error deleting hadron node execution logs: {e}")

        return redirect('user_settings:settings')
