#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: ellma_script_editor_views.py
#  Last Modified: 2024-10-30 17:39:14
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-30 17:39:15
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.ellma.models import EllmaScript
from apps.ellma.utils import ELLMA_TRANSCRIPTION_LANGUAGES
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class EllmaScriptView_ScriptEditor(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        script_id = self.kwargs.get('pk')

        context['ellma_script'] = get_object_or_404(EllmaScript, id=script_id)
        context["ELLMA_TRANSCRIPTION_LANGUAGES"] = ELLMA_TRANSCRIPTION_LANGUAGES

        return context

    def post(self, request, *args, **kwargs):
        # Saving the eLLMa script data.
        script_id = self.kwargs.get('pk')

        ##############################
        # PERMISSION CHECK FOR - UPDATE_ELLMA_SCRIPTS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.UPDATE_ELLMA_SCRIPTS
        ):
            messages.error(self.request, "You do not have permission to update eLLMa scripts.")
            return redirect('ellma:script-editor', pk=script_id)
        ##############################

        ellma_script = get_object_or_404(EllmaScript, id=script_id)

        script_name = request.POST.get('script_name')
        script_content = request.POST.get('script_content')
        transcription_language = request.POST.get('transcription_language')

        try:
            if not script_name or not transcription_language:
                messages.error(request, "Script name and transcription language are required.")
                return redirect('ellma:script-editor', pk=script_id)

            ellma_script.script_name = script_name
            ellma_script.ellma_script_content = script_content
            ellma_script.ellma_transcription_language = transcription_language

            ellma_script.save()

        except Exception as e:
            messages.error(request, f"Error updating script: {e}")
            return redirect('ellma:script-editor', pk=script_id)

        messages.success(request, "Script updated successfully.")
        return redirect('ellma:script-editor', pk=script_id)
