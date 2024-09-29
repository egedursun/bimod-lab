#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: archive_lean_chat_views.py
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
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.multimodal_chat.models import MultimodalLeanChat
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class LeanChatArchiveView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        ##############################
        # PERMISSION CHECK FOR - ARCHIVE_LEAN_CHATS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ARCHIVE_LEAN_CHATS):
            messages.error(self.request, "You do not have permission to archive LeanMod chats.")
            return self.render_to_response(context)
        ##############################

        pk = kwargs.get('pk')
        chat = get_object_or_404(MultimodalLeanChat, id=pk, user=self.request.user)
        chat.is_archived = True
        chat.save()
        return redirect('multimodal_chat:lean_chat')
