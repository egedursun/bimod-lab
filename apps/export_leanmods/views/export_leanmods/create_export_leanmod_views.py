#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_export_leanmod_views.py
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
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.export_leanmods.models import ExportLeanmodAssistantAPI
from apps.leanmod.models import LeanAssistant
from apps.user_permissions.utils import PermissionNames
from config.settings import MAX_LEANMODS_EXPORTS_ORGANIZATION
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class ExportLeanModView_Create(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user_context = self.request.user
        agents = LeanAssistant.objects.filter(
            organization__users__in=[
                user_context
            ]
        )
        context["user"] = user_context
        context["assistants"] = agents
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - CREATE_EXPORT_LEANMOD
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.ADD_EXPORT_LEANMOD
        ):
            messages.error(self.request, "You do not have permission to add Export LeanMod Assistant APIs.")
            return redirect('export_leanmods:list')
        ##############################

        agent_id = request.POST.get('assistant')
        agent = get_object_or_404(LeanAssistant, pk=agent_id)
        is_public = request.POST.get('is_public') == 'on'
        req_limit_hourly = request.POST.get('request_limit_per_hour')

        if ExportLeanmodAssistantAPI.objects.filter(
            created_by_user=request.user
        ).count() > MAX_LEANMODS_EXPORTS_ORGANIZATION:
            logger.error(f"User: {request.user.id} tried to create more than {MAX_LEANMODS_EXPORTS_ORGANIZATION} "
                         f"Export LeanMod Assistant APIs.")

            messages.error(request, f"Maximum number of Export LeanMod Assistant APIs reached for the organization.")
            return self.render_to_response(self.get_context_data())

        if not agent_id or not req_limit_hourly:
            logger.error(
                f"User: {request.user.id} tried to create Export LeanMod Assistant API without required fields.")

            messages.error(request, "LeanMod Assistant ID and Request Limit Per Hour are required.")
            return self.render_to_response(self.get_context_data())

        try:
            new_exp_leanmod = ExportLeanmodAssistantAPI.objects.create(
                lean_assistant_id=agent_id,
                is_public=is_public,
                request_limit_per_hour=req_limit_hourly,
                created_by_user=request.user
            )

            org = agent.organization
            if not org.exported_leanmods:
                org.exported_leanmods.set([new_exp_leanmod])

            else:
                org.exported_leanmods.add(new_exp_leanmod)

            org.save()
            logger.info(f"Export LeanMod Assistant API was created by User: {request.user.id}.")
            messages.success(request, "Export LeanMod Assistant API created successfully!")

            return redirect("export_leanmods:list")

        except Exception as e:
            logger.error(f"Error creating Export LeanMod Assistant API by User: {request.user.id}.")

            messages.error(request, f"Error creating Export LeanMod Assistant API: {str(e)}")
            return self.render_to_response(self.get_context_data())
