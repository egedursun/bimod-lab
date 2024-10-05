#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: delete_lean_chat_views.py
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
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DeleteView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.multimodal_chat.models import MultimodalLeanChat
from apps.multimodal_chat.utils import ChatSourcesNames
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class LeanChatDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'multimodal_chat/chats/confirm_delete_lean_chat.html'
    success_url = '/lean_chat/'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        chat = self.get_object()
        context['chat'] = chat
        return context

    def get_queryset(self):
        return MultimodalLeanChat.objects.filter(user=self.request.user, chat_source=ChatSourcesNames.APP)

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - REMOVE_LEAN_CHATS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.REMOVE_LEAN_CHATS):
            messages.error(self.request, "You do not have permission to remove LeanMod chats.")
            return redirect('multimodal_chat:lean_chat')
        ##############################

        chat = get_object_or_404(MultimodalLeanChat, id=self.kwargs['pk'], user=self.request.user)
        chat.delete()
        return redirect('multimodal_chat:lean_chat')
