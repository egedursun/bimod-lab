#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: delete_export_orchestration_views.py
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
from django.views.generic import DeleteView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.export_orchestrations.models import ExportOrchestrationAPI
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DeleteExportOrchestrationView(LoginRequiredMixin, DeleteView):
    model = ExportOrchestrationAPI
    success_url = 'export_orchestrations:list'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - DELETE_EXPORT_ORCHESTRATION
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_EXPORT_ORCHESTRATION):
            messages.error(self.request, "You do not have permission to delete Export Orchestration APIs.")
            return redirect('export_orchestrations:list')
        ##############################

        export_assistant = get_object_or_404(ExportOrchestrationAPI, id=self.kwargs['pk'])

        export_assistant.delete()
        success_message = "Export Orchestration deleted successfully."
        # remove the exported assistant from the organization
        organization = export_assistant.orchestrator.organization
        organization.exported_orchestrations.remove(export_assistant)
        organization.save()
        print("[DeleteExportOrchestrationsView.post] Export Orchestration deleted successfully.")
        messages.success(request, success_message)
        return redirect(self.success_url)
