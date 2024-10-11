#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: create_export_orchestration_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:46
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.export_orchestrations.management.commands.start_exported_orchestrations import \
    start_endpoint_for_orchestration
from apps.export_orchestrations.models import ExportOrchestrationAPI
from apps.orchestrations.models import Maestro
from apps.user_permissions.utils import PermissionNames
from config.settings import MAX_ORCHESTRATIONS_EXPORTS_ORGANIZATION
from web_project import TemplateLayout


class ExportOrchestrationView_Create(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user_context = self.request.user
        agents = Maestro.objects.filter(organization__users=user_context)
        context["user"] = user_context
        context["assistants"] = agents
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - CREATE_EXPORT_ORCHESTRATION
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_EXPORT_ORCHESTRATION):
            messages.error(self.request, "You do not have permission to add Export Orchestration APIs.")
            return redirect('export_orchestrations:list')
        ##############################

        agent_id = request.POST.get('assistant')
        agent = get_object_or_404(Maestro, pk=agent_id)
        is_public = request.POST.get('is_public') == 'on'
        req_limit_hourly = request.POST.get('request_limit_per_hour')

        if ExportOrchestrationAPI.objects.filter(
            created_by_user=request.user).count() > MAX_ORCHESTRATIONS_EXPORTS_ORGANIZATION:
            messages.error(request, f"Maximum number of Export Orchestration APIs reached for the organization.")
            return self.render_to_response(self.get_context_data())

        if not agent_id or not req_limit_hourly:
            messages.error(request, "Orchestration Assistant ID and Request Limit Per Hour are required.")
            return self.render_to_response(self.get_context_data())

        try:
            new_export_assistant = ExportOrchestrationAPI.objects.create(
                orchestrator_id=agent_id, is_public=is_public, request_limit_per_hour=req_limit_hourly,
                created_by_user=request.user)

            org = agent.organization
            if not org.exported_orchestrations:
                org.exported_orchestrations.set([new_export_assistant])
            else:
                org.exported_orchestrations.add(new_export_assistant)
            org.save()
            start_endpoint_for_orchestration(assistant=new_export_assistant)
            messages.success(request, "Export Orchestration API created successfully!")
            return redirect("export_orchestrations:list")
        except Exception as e:
            messages.error(request, f"Error creating Export Orchestration API: {str(e)}")
            return self.render_to_response(self.get_context_data())
