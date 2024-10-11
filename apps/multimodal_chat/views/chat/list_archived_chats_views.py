#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: list_archived_chats_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:43
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

#
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.message_templates.models import MessageTemplate
from apps.multimodal_chat.models import MultimodalChat
from apps.multimodal_chat.utils import SourcesForMultimodalChatsNames
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from config.settings import MEDIA_URL
from web_project import TemplateLayout


class ChatView_ListArchivedChats(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        active_chat = None
        context_user = self.request.user
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - CREATE_AND_USE_CHATS
        if not UserPermissionManager.is_authorized(user=context_user,
                                                   operation=PermissionNames.CREATE_AND_USE_CHATS):
            messages.error(self.request, "You do not have permission to create and use chats.")
            return context
        ##############################

        if 'chat_id' in self.request.GET:
            active_chat = get_object_or_404(MultimodalChat, id=self.request.GET['chat_id'], user=self.request.user)

        chats = MultimodalChat.objects.filter(
            user=self.request.user, chat_source=SourcesForMultimodalChatsNames.APP,
            is_archived=True
        )

        if active_chat:
            chats = [active_chat] + [chat for chat in chats if chat.id != active_chat.id]
        else:
            if len(chats) > 0:
                active_chat = chats[0]

        agents = Assistant.objects.filter(organization__users=self.request.user)
        orgs = Organization.objects.filter(assistants__in=agents)
        msg_templates = MessageTemplate.objects.filter(user=context_user, organization__in=orgs)
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        active_chat_msgs = active_chat.chat_messages.all().order_by('sent_at') if active_chat else None
        context.update({"chats": chats, "assistants": agents, "active_chat": active_chat,
                        "chat_messages": active_chat_msgs, "message_templates": msg_templates,
                        "base_url": MEDIA_URL})
        return context
