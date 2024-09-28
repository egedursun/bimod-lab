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
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.multimodal_chat.models import MultimodalChat
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class ChatArchiveView(LoginRequiredMixin, TemplateView):
    """
    Handles the archiving of multimodal chats.

    This view allows users to archive specific chats, making them no longer visible in the main chat list but accessible in the archived chats list.

    Methods:
        get_context_data(self, **kwargs): Prepares the context for the chat archiving operation.
        get(self, request, *args, **kwargs): Processes the archiving of the specified chat.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        ##############################
        # PERMISSION CHECK FOR - ARCHIVE_CHATS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ARCHIVE_CHATS):
            messages.error(self.request, "You do not have permission to archive chats.")
            return self.render_to_response(context)
        ##############################

        pk = kwargs.get('pk')
        chat = get_object_or_404(MultimodalChat, id=pk, user=self.request.user)
        chat.is_archived = True
        chat.save()
        return redirect('multimodal_chat:chat')
