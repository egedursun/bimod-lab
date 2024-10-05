#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: list_assistant_memories_views.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:33
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: list_assistant_memories_views.py
#  Last Modified: 2024-09-28 00:53:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:58:32
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.memories.models import AssistantMemory
from apps.memories.utils import MemoryTypeNames
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class ListAssistantMemoryView(TemplateView, LoginRequiredMixin):
    """
    Displays a list of memories for the user's assistants across their organizations.

    This view aggregates both user-specific and assistant-specific memories, organizing them by organization and assistant.

    Methods:
        get_context_data(self, **kwargs): Retrieves the memories associated with the user's assistants and adds them to the context, grouped by organization and assistant.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_ASSISTANT_MEMORIES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_ASSISTANT_MEMORIES):
            messages.error(self.request, "You do not have permission to list assistant memories.")
            return context
        ##############################

        org_assistants = {}
        organizations = Organization.objects.filter(users=self.request.user)
        for organization in organizations:
            assistants = Assistant.objects.filter(organization=organization)
            org_assistants[organization] = []
            for assistant in assistants:
                assistant_specific_memories = AssistantMemory.objects.filter(
                    assistant=assistant,
                    memory_type=MemoryTypeNames.ASSISTANT_SPECIFIC
                )
                user_specific_memories = AssistantMemory.objects.filter(
                    assistant=assistant,
                    memory_type=MemoryTypeNames.USER_SPECIFIC,
                    user=self.request.user
                )
                memories = list(assistant_specific_memories) + list(user_specific_memories)
                org_assistants[organization].extend(memories)

        context['org_assistants'] = org_assistants
        return context
