#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: toggle_service_export_orchestrations_views.py
#  Last Modified: 2024-09-28 15:08:41
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:53:00
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

import importlib

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views import View

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.export_orchestrations.management.commands.start_exported_orchestrations import \
    start_endpoint_for_orchestration
from apps.export_orchestrations.models import ExportOrchestrationAPI
from apps.user_permissions.utils import PermissionNames
from config import settings
from config.settings import EXPORT_ORCHESTRATION_API_BASE_URL


class ToggleExportOrchestrationServiceView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_EXPORT_ORCHESTRATION
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_EXPORT_ORCHESTRATION):
            messages.error(self.request, "You do not have permission to update Export Orchestration APIs.")
            return redirect('export_orchestrations:list')
        ##############################

        export_assistant = get_object_or_404(ExportOrchestrationAPI, pk=self.kwargs['pk'])
        endpoint = EXPORT_ORCHESTRATION_API_BASE_URL + \
                   export_assistant.endpoint.split(EXPORT_ORCHESTRATION_API_BASE_URL)[1]
        api_urls = getattr(importlib.import_module(settings.ROOT_URLCONF), 'urlpatterns')
        export_assistant.is_online = not export_assistant.is_online
        export_assistant.save()

        # Pause or start the endpoint based on the assistant's new online status
        if export_assistant.is_online:
            # check if the endpoint is already in the url patterns
            if not any(endpoint in str(url) for url in api_urls):
                start_endpoint_for_orchestration(export_assistant)
        return redirect('export_orchestrations:list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
