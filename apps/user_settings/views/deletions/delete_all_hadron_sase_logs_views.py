#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_all_hadron_sase_logs_views.py
#  Last Modified: 2024-10-18 21:55:32
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-18 21:55:37
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
from apps.hadron_prime.models import HadronStateErrorActionStateErrorLog
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames

logger = logging.getLogger(__name__)


class SettingsView_DeleteAllHadronNodeSEASELogs(View, LoginRequiredMixin):

    def post(self, request, *args, **kwargs):
        user = request.user
        user_orgs = Organization.objects.filter(users__in=[user])
        hadron_node_sease_logs = HadronStateErrorActionStateErrorLog.objects.filter(
            node__system__organization__in=user_orgs)
        confirmation_field = request.POST.get('confirmation', None)
        if confirmation_field != 'CONFIRM DELETING ALL HADRON NODE SEASE LOGS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL HADRON NODE SEASE LOGS'.")
            logger.error(f"Invalid confirmation field: {confirmation_field}")
            return redirect('user_settings:settings')

        ##############################
        # PERMISSION CHECK FOR - DELETE_HADRON_NODE_SASE_LOGS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_HADRON_NODE_SASE_LOGS):
            messages.error(self.request, "You do not have permission to delete hadron node SEASE logs.")
            return redirect('user_settings:settings')
        ##############################

        try:
            for hadron_sease_log in hadron_node_sease_logs:
                hadron_sease_log.delete()
            logger.info(f"All hadron node SEASE logs associated with User: {user.id} have been deleted.")
            messages.success(request, "All hadron node SEASE logs associated with your account have been deleted.")
        except Exception as e:
            logger.error(f"Error deleting hadron node SEASE logs: {e}")
            messages.error(request, f"Error deleting hadron node SEASE logs: {e}")
        return redirect('user_settings:settings')
