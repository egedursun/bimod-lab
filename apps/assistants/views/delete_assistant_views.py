#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_assistant_views.py
#  Last Modified: 2024-10-05 12:51:58
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:38
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
#
#
import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import DeleteView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class AssistantView_Delete(LoginRequiredMixin, DeleteView):
    model = Assistant

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        agent = self.get_object()
        context['assistant'] = agent
        return context

    def post(self, request, *args, **kwargs):
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - DELETE_ASSISTANTS
        if not UserPermissionManager.is_authorized(user=context_user, operation=PermissionNames.DELETE_ASSISTANTS):
            messages.error(self.request, "You do not have permission to delete agents.")
            return redirect('assistants:list')
        ##############################

        try:
            agent = self.get_object()
            agent.delete()
            logger.info(f"Assistant has been deleted. ")
            messages.success(self.request, "Assistant has been deleted.")
        except Exception as e:
            logger.error(f"[AssistantView_Delete] Error deleting the assistant: {e}")
            messages.error(self.request, "Error deleting the assistant.")

        return redirect('assistants:list')

    def get_queryset(self):
        context_user = self.request.user
        return Assistant.objects.filter(organization__users__in=[context_user])
