#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: toggle_service_export_voidforger_views.py
#  Last Modified: 2024-11-24 21:36:17
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-24 22:07:54
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
from django.shortcuts import redirect, get_object_or_404
from django.views import View

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.export_voidforger.models import ExportVoidForgerAPI
from apps.user_permissions.utils import PermissionNames

logger = logging.getLogger(__name__)


class ExportVoidForgerView_ToggleService(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - UPDATE_EXPORT_VOIDFORGER
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.UPDATE_EXPORT_VOIDFORGER
        ):
            messages.error(self.request, "You do not have permission to update Export VoidForger APIs.")
            return redirect('export_voidforger:list')
        ##############################

        exp_agent = get_object_or_404(ExportVoidForgerAPI, pk=self.kwargs['pk'])
        exp_agent.is_online = not exp_agent.is_online

        exp_agent.save()

        logger.info(f"Export VoidForger was toggled by User: {request.user.id}.")

        return redirect('export_voidforger:list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
