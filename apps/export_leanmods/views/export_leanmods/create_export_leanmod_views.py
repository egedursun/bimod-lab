#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: create_export_leanmod_views.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:39
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: create_export_leanmod_views.py
#  Last Modified: 2024-09-28 00:53:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:51:50
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.export_leanmods.management.commands.start_exported_leanmods import start_endpoint_for_leanmod
from apps.export_leanmods.models import ExportLeanmodAssistantAPI
from apps.leanmod.models import LeanAssistant
from apps.user_permissions.utils import PermissionNames
from config.settings import MAX_LEANMODS_EXPORTS_ORGANIZATION
from web_project import TemplateLayout


class CreateExportLeanmodAssistantsView(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user_context = self.request.user
        assistants = LeanAssistant.objects.filter(organization__users=user_context)
        context["user"] = user_context
        context["assistants"] = assistants
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - CREATE_EXPORT_LEANMOD
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_EXPORT_LEANMOD):
            messages.error(self.request, "You do not have permission to add Export LeanMod Assistant APIs.")
            return redirect('export_leanmods:list')
        ##############################

        assistant_id = request.POST.get('assistant')
        assistant = get_object_or_404(LeanAssistant, pk=assistant_id)
        is_public = request.POST.get('is_public') == 'on'
        request_limit_per_hour = request.POST.get('request_limit_per_hour')

        # check if the number of assistants of the organization is higher than the allowed limit
        if ExportLeanmodAssistantAPI.objects.filter(
            created_by_user=request.user).count() > MAX_LEANMODS_EXPORTS_ORGANIZATION:
            messages.error(request, f"Maximum number of Export LeanMod Assistant APIs reached for the organization.")
            return self.render_to_response(self.get_context_data())

        if not assistant_id or not request_limit_per_hour:
            messages.error(request, "LeanMod Assistant ID and Request Limit Per Hour are required.")
            return self.render_to_response(self.get_context_data())

        try:
            new_export_assistant = ExportLeanmodAssistantAPI.objects.create(
                lean_assistant_id=assistant_id, is_public=is_public, request_limit_per_hour=request_limit_per_hour,
                created_by_user=request.user
            )
            # Add the exported assistant to organization
            organization = assistant.organization
            if not organization.exported_leanmods:
                organization.exported_leanmods.set([new_export_assistant])
            else:
                organization.exported_leanmods.add(new_export_assistant)
            organization.save()
            # Start the endpoint immediately
            start_endpoint_for_leanmod(assistant=new_export_assistant)
            messages.success(request, "Export LeanMod Assistant API created successfully!")
            print("[CreateExportLeanmodAssistantsView.post] Export LeanMod Assistant API created successfully!")
            return redirect("export_leanmods:list")
        except Exception as e:
            messages.error(request, f"Error creating Export LeanMod Assistant API: {str(e)}")
            return self.render_to_response(self.get_context_data())
