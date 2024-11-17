#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_orchestration_views.py
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
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.orchestrations.models import Maestro
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class OrchestrationView_Delete(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        orchestration = get_object_or_404(Maestro, pk=kwargs['pk'])
        context['orchestration'] = orchestration
        return context

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - DELETE_ORCHESTRATIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_ORCHESTRATIONS):
            messages.error(self.request, "You do not have permission to delete orchestrations.")
            return redirect('orchestrations:list')
        ##############################

        orchestration = get_object_or_404(Maestro, pk=kwargs['pk'])
        orchestration_name = orchestration.name

        try:
            orchestration.delete()
        except Exception as e:
            messages.error(request, f"An error occurred while deleting the Orchestration: {str(e)}")
            return redirect("orchestrations:list")

        logger.info(f"Orchestration was deleted by User: {self.request.user.id}.")
        messages.success(request, f'Orchestration "{orchestration_name}" has been successfully deleted.')
        return redirect('orchestrations:list')
