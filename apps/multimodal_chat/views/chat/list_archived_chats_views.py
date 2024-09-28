#  Copyright Policy & Ownership
#
#  Bimod.io is a product of BMD Holdings. All materials, including but not limited to software, code, documentation,
#  graphics, design elements, and user interfaces provided by Bimod.io are protected by copyright law and international
#  treaties.
#  All content within Bimod.io is the exclusive property of BMD Holdings, unless otherwise stated.
#  Unauthorized use, distribution, or reproduction of any material contained in this software without the express
#  written consent of BMD Holdings is strictly prohibited.
#  Users may not copy, modify, distribute, display, perform, or create derivative works of Bimod.io without prior
#  written permission from BMD Holdings.


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.message_templates.models import MessageTemplate
from apps.multimodal_chat.models import MultimodalChat
from apps.multimodal_chat.utils import ChatSourcesNames
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from config.settings import MEDIA_URL
from web_project import TemplateLayout


class ChatArchiveListView(LoginRequiredMixin, TemplateView):
    """
    Displays a list of archived multimodal chats.

    This view retrieves and displays all archived chats for the authenticated user, allowing them to view and interact with archived chat messages.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with the list of archived chats, active chat, and related data.
    """

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
            user=self.request.user, chat_source=ChatSourcesNames.APP,
            # Only show the archived chats
            is_archived=True
        )
        # if there is an active chat, put the active chat at the beginning of the list
        if active_chat:
            chats = [active_chat] + [chat for chat in chats if chat.id != active_chat.id]
        else:
            if len(chats) > 0:
                active_chat = chats[0]

        assistants = Assistant.objects.filter(organization__users=self.request.user)
        organizations = Organization.objects.filter(assistants__in=assistants)
        message_templates = MessageTemplate.objects.filter(user=context_user, organization__in=organizations)
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        active_chat_messages = active_chat.chat_messages.all().order_by('sent_at') if active_chat else None
        context.update(
            {
                "chats": chats, "assistants": assistants, "active_chat": active_chat,
                "chat_messages": active_chat_messages, "message_templates": message_templates, "base_url": MEDIA_URL
            }
        )
        return context
