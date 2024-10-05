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

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.export_orchestrations.management.commands.start_exported_orchestrations import \
    start_endpoint_for_orchestration
from apps.export_orchestrations.models import ExportOrchestrationAPI
from apps.orchestrations.models import Maestro
from apps.user_permissions.utils import PermissionNames
from config.settings import MAX_ORCHESTRATIONS_EXPORTS_ORGANIZATION
from web_project import TemplateLayout


class CreateExportOrchestrationView(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user_context = self.request.user
        assistants = Maestro.objects.filter(organization__users=user_context)
        context["user"] = user_context
        context["assistants"] = assistants
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - CREATE_EXPORT_ORCHESTRATION
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_EXPORT_ORCHESTRATION):
            messages.error(self.request, "You do not have permission to add Export Orchestration APIs.")
            return redirect('export_orchestrations:list')
        ##############################

        assistant_id = request.POST.get('assistant')
        assistant = get_object_or_404(Maestro, pk=assistant_id)
        is_public = request.POST.get('is_public') == 'on'
        request_limit_per_hour = request.POST.get('request_limit_per_hour')

        # check if the number of assistants of the organization is higher than the allowed limit
        if ExportOrchestrationAPI.objects.filter(
            created_by_user=request.user).count() > MAX_ORCHESTRATIONS_EXPORTS_ORGANIZATION:
            messages.error(request, f"Maximum number of Export Orchestration APIs reached for the organization.")
            return self.render_to_response(self.get_context_data())

        if not assistant_id or not request_limit_per_hour:
            messages.error(request, "Orchestration Assistant ID and Request Limit Per Hour are required.")
            return self.render_to_response(self.get_context_data())

        try:
            new_export_assistant = ExportOrchestrationAPI.objects.create(
                orchestrator_id=assistant_id, is_public=is_public, request_limit_per_hour=request_limit_per_hour,
                created_by_user=request.user
            )
            # Add the exported orchestration to organization
            organization = assistant.organization
            if not organization.exported_orchestrations:
                organization.exported_orchestrations.set([new_export_assistant])
            else:
                organization.exported_orchestrations.add(new_export_assistant)
            organization.save()
            # Start the endpoint immediately
            start_endpoint_for_orchestration(assistant=new_export_assistant)
            messages.success(request, "Export Orchestration API created successfully!")
            print("[CreateExportOrchestrationsView.post] Export Orchestration API created successfully!")
            return redirect("export_orchestrations:list")
        except Exception as e:
            messages.error(request, f"Error creating Export Orchestration API: {str(e)}")
            return self.render_to_response(self.get_context_data())
