#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_export_assistant_views.py
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
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.user_permissions.utils import PermissionNames
from config.settings import MAX_ASSISTANT_EXPORTS_ORGANIZATION
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class ExportAssistantView_Create(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user_context = self.request.user
        agents = Assistant.objects.filter(
            organization__users__in=[
                user_context
            ]
        )
        context["user"] = user_context
        context["assistants"] = agents
        return context

    def post(self, request, *args, **kwargs):
        from apps.export_assistants.models import ExportAssistantAPI

        ##############################
        # PERMISSION CHECK FOR - ADD_EXPORT_ASSISTANT
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.ADD_EXPORT_ASSISTANT
        ):
            messages.error(self.request, "You do not have permission to add Export Assistant APIs.")
            return redirect('export_assistants:list')
        ##############################

        agent_id = request.POST.get('assistant')
        agent = get_object_or_404(Assistant, pk=agent_id)
        is_public = request.POST.get('is_public') == 'on'
        limit_req_per_hour = request.POST.get('request_limit_per_hour')

        if ExportAssistantAPI.objects.filter(
            created_by_user=request.user
        ).count() > MAX_ASSISTANT_EXPORTS_ORGANIZATION:
            messages.error(request, f"Maximum number of Export Assistant APIs reached for the organization.")
            return self.render_to_response(self.get_context_data())

        if not agent_id or not limit_req_per_hour:
            messages.error(request, "Assistant ID and Request Limit Per Hour are required.")
            return self.render_to_response(self.get_context_data())

        try:
            new_export_assistant = ExportAssistantAPI.objects.create(
                assistant_id=agent_id,
                is_public=is_public,
                request_limit_per_hour=limit_req_per_hour,
                created_by_user=request.user
            )

            org = agent.organization
            org.exported_assistants.add(new_export_assistant)
            org.save()

            logger.info(f"Export Assistant API was created by User: {request.user.id}.")
            messages.success(request, "Export Assistant API created successfully!")
            return redirect("export_assistants:list")

        except Exception as e:

            logger.error(f"Error creating Export Assistant API: {str(e)}")
            messages.error(request, f"Error creating Export Assistant API: {str(e)}")
            return self.render_to_response(self.get_context_data())
