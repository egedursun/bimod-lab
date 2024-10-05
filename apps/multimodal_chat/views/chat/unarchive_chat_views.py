#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: unarchive_chat_views.py
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
#  File: unarchive_chat_views.py
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
from apps.multimodal_chat.models import MultimodalChat
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class ChatUnarchiveView(LoginRequiredMixin, TemplateView):
    """
    Handles the unarchiving of multimodal chats.

    This view allows users to unarchive specific chats, making them visible again in the main chat list.

    Methods:
        get_context_data(self, **kwargs): Prepares the context for the chat unarchiving operation.
        get(self, request, *args, **kwargs): Processes the unarchiving of the specified chat.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        ##############################
        # PERMISSION CHECK FOR - UNARCHIVE_CHATS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UNARCHIVE_CHATS):
            messages.error(self.request, "You do not have permission to archive chats.")
            return self.render_to_response(context)
        ##############################

        pk = kwargs.get('pk')
        chat = get_object_or_404(MultimodalChat, id=pk, user=self.request.user)
        chat.is_archived = False
        chat.save()
        return redirect('multimodal_chat:chat')
