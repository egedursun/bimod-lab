#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: update_export_assistants_views.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:42
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
#  File: update_export_assistants_views.py
#  Last Modified: 2024-09-28 00:53:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:50:40
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.export_assistants.models import ExportAssistantAPI
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class UpdateExportAssistantsView(TemplateView, LoginRequiredMixin):
    """
    Handles updating an existing Export Assistant API.

    This view allows users with the appropriate permissions to modify an existing Export Assistant API's attributes, such as request limits and public availability.

    Methods:
        get_context_data(self, **kwargs): Retrieves the current Export Assistant API details and adds them to the context, along with other relevant data such as available assistants.
        post(self, request, *args, **kwargs): Processes the form submission for updating the Export Assistant API, including permission checks and validation.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        export_assistant = get_object_or_404(ExportAssistantAPI, pk=self.kwargs['pk'])
        context['export_assistant'] = export_assistant
        context['assistants'] = Assistant.objects.filter(
            organization__users__in=[self.request.user]).all()
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_EXPORT_ASSISTANT
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_EXPORT_ASSIST):
            messages.error(self.request, "You do not have permission to update Export Assistant APIs.")
            return redirect('export_assistants:list')
        ##############################

        export_assistant = get_object_or_404(ExportAssistantAPI, pk=self.kwargs['pk'])
        export_assistant.assistant_id = request.POST.get('assistant')
        export_assistant.request_limit_per_hour = request.POST.get('request_limit_per_hour')
        export_assistant.is_public = request.POST.get('is_public') == 'on'
        if export_assistant.assistant_id and export_assistant.request_limit_per_hour:
            export_assistant.save()
            messages.success(request, "Export Assistant updated successfully.")
            print("[UpdateExportAssistantsView.post] Export Assistant updated successfully!")
            return redirect('export_assistants:list')
        else:
            messages.error(request, "There was an error updating the Export Assistant.")

        context = self.get_context_data()
        context.update({
            'export_assistant': export_assistant,
            'assistants': Assistant.objects.filter(organization__users__in=[self.request.user]).all()
        })
        return render(request, self.template_name, context)
