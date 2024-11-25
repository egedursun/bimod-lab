#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: update_export_voidforger_views.py
#  Last Modified: 2024-11-24 21:36:17
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-24 22:08:42
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
from apps.export_voidforger.models import ExportVoidForgerAPI
from apps.user_permissions.utils import PermissionNames
from apps.voidforger.models import VoidForger
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class ExportVoidForgerView_Update(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        exp_agent = get_object_or_404(
            ExportVoidForgerAPI,
            pk=self.kwargs['pk']
        )

        context['export_assistant'] = exp_agent

        context['assistants'] = VoidForger.objects.filter(
            llm_model__organization__users__in=[self.request.user]
        )

        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_EXPORT_VOIDFORGER
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.UPDATE_EXPORT_VOIDFORGER
        ):
            messages.error(self.request, "You do not have permission to update Export VoidForger APIs.")
            return redirect('export_voidforger:list')
        ##############################

        exp_agent = get_object_or_404(
            ExportVoidForgerAPI,
            pk=self.kwargs['pk']
        )

        exp_agent: ExportVoidForgerAPI
        exp_agent.voidforger_id = request.POST.get('assistant')
        exp_agent.request_limit_per_hour = request.POST.get('request_limit_per_hour')
        exp_agent.is_public = request.POST.get('is_public') == 'on'

        if exp_agent.voidforger_id and exp_agent.request_limit_per_hour:
            exp_agent.save()
            messages.success(request, "Export VoidForger updated successfully.")

            return redirect('export_voidforger:list')

        else:
            messages.error(request, "There was an error updating the Export VoidForger.")

        context = self.get_context_data()
        context.update(
            {
                'export_assistant': exp_agent,
                'assistants': VoidForger.objects.filter(
                    llm_model__organization__users__in=[self.request.user]
                ).all()
            }
        )

        logger.error(f"Export VoidForger was not updated by User: {request.user.id}.")
        return render(request, self.template_name, context)
