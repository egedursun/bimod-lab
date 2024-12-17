#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: clean_chat_history_views.py
#  Last Modified: 2024-12-17 00:34:32
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-17 00:34:32
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

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)
from django.shortcuts import redirect
from django.urls import reverse

from django.views import View

from apps.multimodal_chat.models import (
    MultimodalChatMessage
)

logger = logging.getLogger(__name__)


class ChatView_ChatCleanHistory(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        chat_id = kwargs.get('pk')

        if not chat_id:
            logger.error("Chat id not provided.")

            messages.error(
                request,
                "Chat id not provided."
            )

            return redirect("multimodal_chat:chat")

        try:

            chat_messages = MultimodalChatMessage.objects.filter(
                multimodal_chat_id=chat_id
            )

            chat_messages.delete()

        except Exception as e:
            logger.error(f"Error while cleaning chat history: {e}")

            messages.error(
                request,
                "Error while cleaning chat history."
            )

        base_url = reverse("multimodal_chat:chat")
        query_string = f"?chat_id={chat_id}"
        url = f"{base_url}{query_string}"

        logger.info(f"Chat history cleaned for chat with id {chat_id}.")

        messages.success(
            request,
            "Chat history has been cleaned successfully."
        )

        return redirect(url)
