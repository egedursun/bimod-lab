#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: narrate_chat_message_views.py
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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from apps._services.llms.llm_decoder import InternalLLMClient
from apps.multimodal_chat.models import MultimodalChatMessage


class ChatMessageNarrationView(LoginRequiredMixin, View):
    """
    Handles the narration of chat messages.

    This view allows users to listen to the narration of chat messages using text-to-speech (TTS) functionality.
    """

    def get(self, request, *args, **kwargs):
        message_id = kwargs.get('pk')
        try:
            message = get_object_or_404(MultimodalChatMessage, id=message_id, multimodal_chat__user=request.user)
        except Exception as e:
            print(f"[ChatMessageNarrationView.get] Error while getting the chat message: {e}")
            return JsonResponse({'audio_url': None})

        try:
            if message.message_audio:
                return JsonResponse({'audio_url': message.message_audio})
        except Exception as e:
            print(f"[ChatMessageNarrationView.get] Error while getting the audio URL: {e}")
            pass

        # Assuming 'InternalLLMClient.text_to_audio_message' returns a dict with 'audio_url'
        try:
            response = InternalLLMClient.get(assistant=message.multimodal_chat.assistant,
                                             multimodal_chat=message.multimodal_chat).text_to_audio_message(
                message=message)
        except Exception as e:
            print(f"[ChatMessageNarrationView.get] Error while narrating the chat message: {e}")
            return JsonResponse({'audio_url': None})

        try:
            message.message_audio = response['audio_url']
            message.save()
        except Exception as e:
            print(f"[ChatMessageNarrationView.get] Error while saving the audio URL: {e}")
            pass

        return JsonResponse({'audio_url': response['audio_url']})
