#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_voidforger_chat_views.py
#  Last Modified: 2024-11-14 22:31:35
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-15 18:53:06
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
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DeleteView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.multimodal_chat.utils import SourcesForMultimodalChatsNames
from apps.user_permissions.utils import PermissionNames
from apps.voidforger.models import MultimodalVoidForgerChat
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class VoidForgerView_DeleteVoidForgerChat(LoginRequiredMixin, DeleteView):
    template_name = 'voidforger/chats/voidforger_confirm_delete_chat.html'
    success_url = '/workspace/'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        chat = self.get_object()
        context['chat'] = chat
        return context

    def get_queryset(self):
        return MultimodalVoidForgerChat.objects.filter(
            user=self.request.user,
            chat_source=SourcesForMultimodalChatsNames.APP
        )

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - REMOVE_VOIDFORGER_CHATS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.REMOVE_VOIDFORGER_CHATS
        ):
            messages.error(self.request, "You do not have permission to remove VoidForger Chats.")
            return redirect('multimodal_chat:main_workspace')
        ##############################

        chat = get_object_or_404(
            MultimodalVoidForgerChat,
            id=self.kwargs['pk'],
            user=self.request.user
        )

        try:
            chat.delete()

        except Exception as e:
            logger.error(f"VoidForger chat deletion failed. Error: {e}")
            messages.error(request, f'The VoidForger chat could not be deleted.')
            return redirect('multimodal_chat:main_workspace')

        logger.info(f"VoidForger chat was deleted by User: {self.request.user.id}.")
        return redirect('multimodal_chat:main_workspace')
