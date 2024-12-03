#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_archived_lean_chats_views.py
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
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.leanmod.models import LeanAssistant
from apps.message_templates.models import MessageTemplate
from apps.multimodal_chat.models import MultimodalLeanChat
from apps.multimodal_chat.utils import SourcesForMultimodalChatsNames
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from config.settings import MEDIA_URL
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class ChatView_LeanChatListArchivedChats(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        active_chat = None
        context_user = self.request.user
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - CREATE_AND_USE_LEAN_CHATS
        if not UserPermissionManager.is_authorized(
            user=context_user,
            operation=PermissionNames.CREATE_AND_USE_LEAN_CHATS
        ):
            messages.error(self.request, "You do not have permission to create and use LeanMod chats.")
            return context
        ##############################

        if 'chat_id' in self.request.GET:
            active_chat = get_object_or_404(
                MultimodalLeanChat,
                id=self.request.GET['chat_id'],
                user=self.request.user
            )

        chats = MultimodalLeanChat.objects.filter(
            user=self.request.user,
            chat_source=SourcesForMultimodalChatsNames.APP,
            is_archived=True
        )

        if active_chat:
            chats = [active_chat] + [chat for chat in chats if chat.id != active_chat.id]

        else:
            if len(chats) > 0:
                active_chat = chats[0]

        lean_agents = LeanAssistant.objects.filter(
            organization__users=self.request.user
        )

        orgs = Organization.objects.filter(
            lean_assistants__in=lean_agents
        )

        msg_templates = MessageTemplate.objects.filter(
            user=context_user,
            organization__in=orgs
        )

        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        active_chat_msgs = active_chat.lean_chat_messages.all().order_by('sent_at') if active_chat else None

        context.update(
            {
                "chats": chats,
                "assistants": lean_agents,
                "active_chat": active_chat,
                "chat_messages": active_chat_msgs,
                "message_templates": msg_templates,
                "base_url": MEDIA_URL
            }
        )

        logger.info(f"LeanMod chats were listed for User: {self.request.user.id}.")
        return context
