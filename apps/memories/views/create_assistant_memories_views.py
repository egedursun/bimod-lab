#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: create_assistant_memories_views.py
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
#   For permission inquiries, please contact: admin@br6.in.
#

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.memories.models import AssistantMemory
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class AssistantMemoryView_Create(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user
        agents = Assistant.objects.filter(organization__users=user)
        context.update({'assistants': agents})
        return context

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - ADD_ASSISTANT_MEMORIES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_ASSISTANT_MEMORIES):
            messages.error(self.request, "You do not have permission to add assistant memories.")
            return redirect('memories:list')
        ##############################

        agent_id = request.POST.get('assistant')
        memory_type = request.POST.get('memory_type')
        memory_text_content = request.POST.get('memory_text_content')

        AssistantMemory.objects.create(user=request.user, assistant_id=agent_id, memory_type=memory_type,
                                       memory_text_content=memory_text_content)

        agent = Assistant.objects.get(id=agent_id)
        agent.memories.add(AssistantMemory.objects.last())
        return redirect('memories:list')
