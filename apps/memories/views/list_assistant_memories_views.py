#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: list_assistant_memories_views.py
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
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.memories.models import AssistantMemory
from apps.memories.utils import AgentStandardMemoryTypesNames
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class AssistantMemoryView_List(TemplateView, LoginRequiredMixin):
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
        orgs = Organization.objects.filter(users=self.request.user)
        for org in orgs:
            agents = Assistant.objects.filter(organization=org)
            org_assistants[org] = []
            for agent in agents:
                agent_spec_mems = AssistantMemory.objects.filter(
                    assistant=agent, memory_type=AgentStandardMemoryTypesNames.ASSISTANT_SPECIFIC)
                user_spec_mems = AssistantMemory.objects.filter(
                    assistant=agent, memory_type=AgentStandardMemoryTypesNames.USER_SPECIFIC, user=self.request.user)
                memories = list(agent_spec_mems) + list(user_spec_mems)
                org_assistants[org].extend(memories)
        context['org_assistants'] = org_assistants
        return context
