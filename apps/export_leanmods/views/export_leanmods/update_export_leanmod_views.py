#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.export_leanmods.models import ExportLeanmodAssistantAPI
from apps.leanmod.models import LeanAssistant
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class ExportLeanModView_Update(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        exp_agent = get_object_or_404(ExportLeanmodAssistantAPI, pk=self.kwargs['pk'])
        context['export_assistant'] = exp_agent

        context['assistants'] = LeanAssistant.objects.filter(
            organization__users__in=[
                self.request.user
            ]
        )

        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_EXPORT_LEANMOD
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.UPDATE_EXPORT_LEANMOD
        ):
            messages.error(self.request, "You do not have permission to update Export LeanMod Assistant APIs.")
            return redirect('export_leanmods:list')
        ##############################

        exp_agent = get_object_or_404(
            ExportLeanmodAssistantAPI,
            pk=self.kwargs['pk']
        )

        exp_agent: ExportLeanmodAssistantAPI

        exp_agent.lean_assistant_id = request.POST.get('assistant')
        exp_agent.request_limit_per_hour = request.POST.get('request_limit_per_hour')
        exp_agent.is_public = request.POST.get('is_public') == 'on'

        if exp_agent.lean_assistant_id and exp_agent.request_limit_per_hour:

            exp_agent.save()

            logger.info(f"Export LeanMod Assistant was updated by User: {request.user.id}.")
            messages.success(request, "Export LeanMod Assistant updated successfully.")

            return redirect('export_leanmods:list')

        else:
            logger.error(f"Export LeanMod Assistant was not updated by User: {request.user.id}.")
            messages.error(request, "There was an error updating the LeanMod Export Assistant.")

        context = self.get_context_data()

        context.update(
            {
                'export_assistant': exp_agent,
                'assistants': LeanAssistant.objects.filter(
                    organization__users__in=[
                        self.request.user
                    ]
                ).all()
            })

        return render(request, self.template_name, context)
