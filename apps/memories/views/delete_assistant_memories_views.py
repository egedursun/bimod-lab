#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_assistant_memories_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:34
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
from django.views.generic import DeleteView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.memories.models import AssistantMemory
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class AssistantMemoryView_Delete(LoginRequiredMixin, DeleteView):
    model = AssistantMemory
    success_url = 'memories:list'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - DELETE_ASSISTANT_MEMORIES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_ASSISTANT_MEMORIES):
            messages.error(self.request, "You do not have permission to delete assistant memories.")
            return redirect('memories:list')
        ##############################

        memory = get_object_or_404(AssistantMemory, id=self.kwargs['pk'])

        try:
            memory.delete()
        except Exception as e:
            logger.error(f"Error deleting Assistant Memory: {e}")
            return redirect(self.success_url)

        success_message = "Memory deleted successfully!"
        messages.success(request, success_message)
        logger.info(f"Assistant Memory was deleted by User: {self.request.user.id}.")
        return redirect(self.success_url)
