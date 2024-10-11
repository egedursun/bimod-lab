#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: list_starred_messages_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:44
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.starred_messages.models import StarredMessage
from apps.user_permissions.utils import PermissionNames
from config.settings import MEDIA_URL
from web_project import TemplateLayout


class StarredMessageView_List(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_STARRED_MESSAGES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_STARRED_MESSAGES):
            messages.error(self.request, "You do not have permission to view starred messages.")
            return context
        ##############################

        user = self.request.user
        starred_msgs = StarredMessage.objects.filter(user=user).select_related('chat_message', 'assistant',
                                                                                   'organization', 'chat')
        org_agents_msgs = {}
        for msg in starred_msgs:
            org_name = msg.organization.name
            agent_name = msg.assistant.name
            if org_name not in org_agents_msgs:
                org_agents_msgs[org_name] = {}
            if agent_name not in org_agents_msgs[org_name]:
                org_agents_msgs[org_name][agent_name] = []
            org_agents_msgs[org_name][agent_name].append(msg)
        context.update({'org_assistants_messages': org_agents_msgs, 'base_url': MEDIA_URL})
        return context
