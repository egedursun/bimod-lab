#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: toggle_service_export_assistants_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:44
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
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.export_assistants.models import ExportAssistantAPI
from apps.user_permissions.utils import PermissionNames

logger = logging.getLogger(__name__)


class ExportAssistantView_ToggleService(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):

        exp_agent = get_object_or_404(ExportAssistantAPI, pk=self.kwargs['pk'])
        context_user = request.user

        ##############################
        # PERMISSION CHECK FOR - UPDATE_EXPORT_ASSISTANT
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.UPDATE_EXPORT_ASSIST
        ):
            messages.error(self.request, "You do not have permission to update Export Assistant APIs.")
            return redirect('export_assistants:list')
        ##############################

        try:
            exp_agent.is_online = not exp_agent.is_online
            exp_agent.save()

        except Exception as e:
            logger.error(f"Error toggling Export Assistant: {e}")
            messages.error(request, "Error toggling Export Assistant.")

            return redirect('export_assistants:list')

        logger.info(f"Export Assistant was toggled by User: {context_user.id}.")

        return redirect('export_assistants:list')

    def get(self, request, *args, **kwargs):

        return self.post(request, *args, **kwargs)
