#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: purge_action_memory_logs_views.py
#  Last Modified: 2024-11-14 22:32:32
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-15 18:56:53
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


class VoidForgerView_PurgeActionMemoryLogs(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - DELETE_VOIDFORGER_ACTION_MEMORY_LOGS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_VOIDFORGER_ACTION_MEMORY_LOGS):
            messages.error(self.request, "You do not have permission to delete VoidForger Action Memory Logs.")
            return redirect('voidforger:list_action_memory_logs')
        ##############################

        try:
            voidforger_id = kwargs.get('voidforger_id')
            voidforger = VoidForger.objects.get(id=voidforger_id)
            action_memory_logs = voidforger.voidforgeractionmemorylog_set.all()
            for action_memory_log in action_memory_logs:
                action_memory_log.delete()
        except Exception as e:
            messages.error(request, f"Error purging action memory logs: {e}")
            return redirect('voidforger:list_action_memory_logs')

        messages.success(request, "Action memory logs purged successfully.")
        return redirect('voidforger:list_action_memory_logs')
