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

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.memories.models import AssistantMemory
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class CreateAssistantMemoryView(TemplateView, LoginRequiredMixin):
    """
    Handles the creation of new memories for an assistant.

    This view allows users to create new memories, which can be either user-specific or assistant-specific, depending on the selected memory type.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with the assistants associated with the current user.
        post(self, request, *args, **kwargs): Processes the form submission to create a new memory and associates it with the selected assistant.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user
        assistants = Assistant.objects.filter(organization__users=user)
        context.update({'assistants': assistants})
        return context

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - ADD_ASSISTANT_MEMORIES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_ASSISTANT_MEMORIES):
            messages.error(self.request, "You do not have permission to add assistant memories.")
            return redirect('memories:list')
        ##############################

        assistant_id = request.POST.get('assistant')
        memory_type = request.POST.get('memory_type')
        memory_text_content = request.POST.get('memory_text_content')

        AssistantMemory.objects.create(
            user=request.user, assistant_id=assistant_id, memory_type=memory_type,
            memory_text_content=memory_text_content
        )
        # add the memory to the assistant memories
        # Note: the specificity of the memory is handled in prompt management module
        assistant = Assistant.objects.get(id=assistant_id)
        assistant.memories.add(AssistantMemory.objects.last())
        print('[CreateAssistantMemoryView.post] Memory created successfully.')
        return redirect('memories:list')
