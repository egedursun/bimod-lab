#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: update_export_assistants_views.py
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
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.export_assistants.models import ExportAssistantAPI
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class ExportAssistantView_Update(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        exp_agent = get_object_or_404(
            ExportAssistantAPI,
            pk=self.kwargs['pk']
        )

        context['export_assistant'] = exp_agent
        context['assistants'] = Assistant.objects.filter(
            organization__users__in=[
                self.request.user
            ]
        ).all()

        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_EXPORT_ASSISTANT
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.UPDATE_EXPORT_ASSIST
        ):
            messages.error(self.request, "You do not have permission to update Export Assistant APIs.")
            return redirect('export_assistants:list')
        ##############################

        exp_agent = get_object_or_404(ExportAssistantAPI, pk=self.kwargs['pk'])

        try:
            exp_agent.assistant_id = request.POST.get('assistant')
            exp_agent.request_limit_per_hour = request.POST.get('request_limit_per_hour')
            exp_agent.is_public = request.POST.get('is_public') == 'on'

            if exp_agent.assistant_id and exp_agent.request_limit_per_hour:
                exp_agent.save()
                logger.info(f"Export Assistant was updated by User: {request.user.id}.")
                messages.success(request, "Export Assistant updated successfully.")
                return redirect('export_assistants:list')

            else:
                logger.error(f"Error updating Export Assistant by User: {request.user.id}.")
                messages.error(request, "There was an error updating the Export Assistant.")

        except Exception as e:
            logger.error(f"Error updating Export Assistant: {e}")
            messages.error(request, "Error updating Export Assistant.")

            return redirect('export_assistants:list')

        context = self.get_context_data()
        context.update({
            'export_assistant': exp_agent,
            'assistants': Assistant.objects.filter(
                organization__users__in=[
                    self.request.user
                ]
            ).all()
        })

        return render(request, self.template_name, context)
