#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#
import logging

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


logger = logging.getLogger(__name__)


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

        org_memories = {}
        orgs = Organization.objects.filter(users=self.request.user)
        for org in orgs:
            agents = Assistant.objects.filter(organization=org)
            org_memories[org] = []
            for agent in agents:
                organization_spec_mems = AssistantMemory.objects.filter(
                    organization=org, assistant=agent, memory_type=AgentStandardMemoryTypesNames.ORGANIZATION_SPECIFIC)
                agent_spec_mems = AssistantMemory.objects.filter(
                    organization=org, assistant=agent, memory_type=AgentStandardMemoryTypesNames.ASSISTANT_SPECIFIC)
                user_spec_mems = AssistantMemory.objects.filter(
                    organization=org, assistant=agent, memory_type=AgentStandardMemoryTypesNames.USER_SPECIFIC, user=self.request.user)
                memories = list(organization_spec_mems) + list(agent_spec_mems) + list(set(user_spec_mems))
                org_memories[org].extend(memories)
        context['org_assistants'] = org_memories
        logger.info(f"Assistant Memories were listed by User: {self.request.user.id}.")
        return context
