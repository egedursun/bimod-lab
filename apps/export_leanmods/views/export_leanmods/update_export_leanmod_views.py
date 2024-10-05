#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: update_export_leanmod_views.py
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.export_leanmods.models import ExportLeanmodAssistantAPI
from apps.leanmod.models import LeanAssistant
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class UpdateExportLeanmodAssistantsView(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        export_assistant = get_object_or_404(ExportLeanmodAssistantAPI, pk=self.kwargs['pk'])
        context['export_assistant'] = export_assistant
        context['assistants'] = LeanAssistant.objects.filter(
            organization__users__in=[self.request.user]
        )
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_EXPORT_LEANMOD
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_EXPORT_LEANMOD):
            messages.error(self.request, "You do not have permission to update Export LeanMod Assistant APIs.")
            return redirect('export_leanmods:list')
        ##############################

        export_assistant = get_object_or_404(ExportLeanmodAssistantAPI, pk=self.kwargs['pk'])
        export_assistant: ExportLeanmodAssistantAPI
        export_assistant.lean_assistant_id = request.POST.get('assistant')
        export_assistant.request_limit_per_hour = request.POST.get('request_limit_per_hour')
        export_assistant.is_public = request.POST.get('is_public') == 'on'
        if export_assistant.lean_assistant_id and export_assistant.request_limit_per_hour:
            export_assistant.save()
            messages.success(request, "Export LeanMod Assistant updated successfully.")
            print("[UpdateExportLeanmodAssistantsView.post] Export LeanMod Assistant updated successfully!")
            return redirect('export_leanmods:list')
        else:
            messages.error(request, "There was an error updating the LeanMod Export Assistant.")

        context = self.get_context_data()
        context.update(
            {
                'export_assistant': export_assistant,
                'assistants': LeanAssistant.objects.filter(organization__users__in=[self.request.user]).all()
            })
        return render(request, self.template_name, context)
