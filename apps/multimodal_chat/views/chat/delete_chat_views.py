#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: delete_chat_views.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:41
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
#  File: delete_chat_views.py
#  Last Modified: 2024-09-28 20:38:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:06:05
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

#
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DeleteView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.multimodal_chat.models import MultimodalChat
from apps.multimodal_chat.utils import ChatSourcesNames
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class ChatDeleteView(LoginRequiredMixin, DeleteView):
    """
    Handles the deletion of multimodal chats.

    This view allows users to delete specific chats after confirming the action. Only chats that belong to the authenticated user can be deleted.

    Methods:
        get_context_data(self, **kwargs): Prepares the context for the chat deletion confirmation page.
        get_queryset(self): Filters the queryset to only include chats that belong to the authenticated user.
        post(self, request, *args, **kwargs): Processes the deletion of the specified chat.
    """

    template_name = 'multimodal_chat/chats/confirm_delete_chat.html'
    success_url = '/chat/'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        chat = self.get_object()
        context['chat'] = chat
        return context

    def get_queryset(self):
        return MultimodalChat.objects.filter(user=self.request.user, chat_source=ChatSourcesNames.APP)

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - REMOVE_CHATS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.REMOVE_CHATS):
            messages.error(self.request, "You do not have permission to remove chats.")
            return redirect('multimodal_chat:chat')
        ##############################

        chat = get_object_or_404(MultimodalChat, id=self.kwargs['pk'], user=self.request.user)
        chat.delete()
        return redirect('multimodal_chat:chat')
