#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_auto_execution_logs_views.py
#  Last Modified: 2024-11-14 22:31:35
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-15 18:56:30
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
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.user_permissions.utils import PermissionNames
from apps.voidforger.models import VoidForger
from web_project import TemplateLayout


class VoidForgerView_ListVoidForgerAutoExecutionLogs(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - LIST_VOIDFORGER_AUTO_EXECUTION_MEMORY_LOGS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_VOIDFORGER_AUTO_EXECUTION_MEMORY_LOGS):
            messages.error(self.request, "You do not have permission to list VoidForger Auto Execution Memory Logs.")
            return context
        ##############################

        voidforger = VoidForger.objects.get(user=user)
        auto_execution_logs = voidforger.voidforgertoggleautoexecutionlog_set.all().order_by('-timestamp')

        # Paginate logs
        paginator = Paginator(auto_execution_logs, 10)
        page = self.request.GET.get('page', 1)
        try:
            logs = paginator.page(page)
        except PageNotAnInteger:
            logs = paginator.page(1)
        except EmptyPage:
            logs = paginator.page(paginator.num_pages)

        context['auto_execution_logs'] = logs
        context['voidforger'] = voidforger
        return context
