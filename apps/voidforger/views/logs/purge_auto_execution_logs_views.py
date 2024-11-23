#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: purge_auto_execution_logs_views.py
#  Last Modified: 2024-11-14 22:32:32
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-15 18:57:06
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.user_permissions.utils import PermissionNames
from apps.voidforger.models import VoidForger


class VoidForgerView_PurgeAutoExecutionLogs(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - DELETE_VOIDFORGER_AUTO_EXECUTION_MEMORY_LOGS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_VOIDFORGER_AUTO_EXECUTION_MEMORY_LOGS
        ):
            messages.error(self.request, "You do not have permission to delete VoidForger Auto Execution Memory Logs.")
            return redirect('voidforger:list_auto_execution_logs')
        ##############################

        try:
            voidforger_id = kwargs.get('voidforger_id')
            voidforger = VoidForger.objects.get(id=voidforger_id)
            auto_execution_memory_logs = voidforger.voidforgertoggleautoexecutionlog_set.all()

            for auto_execution_memory_log in auto_execution_memory_logs:
                auto_execution_memory_log.delete()

        except Exception as e:
            messages.error(request, f"Error purging auto execution memory logs: {e}")
            return redirect('voidforger:list_auto_execution_logs')

        messages.success(request, "Auto execution memory logs purged successfully.")
        return redirect('voidforger:list_auto_execution_logs')
