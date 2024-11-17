#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: toggle_service_export_leanmods_views.py
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

import importlib
import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views import View

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.export_leanmods.management.commands.start_exported_leanmods import start_endpoint_for_leanmod
from apps.export_leanmods.models import ExportLeanmodAssistantAPI
from apps.user_permissions.utils import PermissionNames
from config import settings
from config.settings import EXPORT_LEANMOD_API_BASE_URL

logger = logging.getLogger(__name__)


class ExportLeanModView_ToggleService(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_EXPORT_LEANMOD
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_EXPORT_LEANMOD):
            messages.error(self.request, "You do not have permission to update Export LeanMod Assistant APIs.")
            return redirect('export_leanmods:list')
        ##############################

        try:
            exp_agent = get_object_or_404(ExportLeanmodAssistantAPI, pk=self.kwargs['pk'])
            endpoint = EXPORT_LEANMOD_API_BASE_URL + exp_agent.endpoint.split(EXPORT_LEANMOD_API_BASE_URL)[1]
            api_urls = getattr(importlib.import_module(settings.ROOT_URLCONF), 'urlpatterns')
            exp_agent.is_online = not exp_agent.is_online
            exp_agent.save()
            if exp_agent.is_online:
                if not any(endpoint in str(url) for url in api_urls):
                    start_endpoint_for_leanmod(exp_agent)
        except Exception as e:
            logger.error(f"Error toggling Export LeanMod Assistant: {e}")
            messages.error(request, "Error toggling Export LeanMod Assistant.")
            return redirect('export_leanmods:list')

        logger.info(f"Export LeanMod Assistant was toggled by User: {request.user.id}.")
        return redirect('export_leanmods:list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
