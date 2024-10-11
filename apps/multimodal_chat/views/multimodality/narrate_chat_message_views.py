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


from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from apps.core.generative_ai.auxiliary_clients.auxiliary_llm_audio_client import AuxiliaryLLMAudioClient
from apps.multimodal_chat.models import MultimodalChatMessage


class LeanChat_MessageNarration(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        msg_id = kwargs.get('pk')
        try:
            msg = get_object_or_404(MultimodalChatMessage, id=msg_id, multimodal_chat__user=request.user)
        except Exception as e:
            return JsonResponse({'audio_url': None})
        try:
            if msg.message_audio:
                return JsonResponse({'audio_url': msg.message_audio})
        except Exception as e:
            pass
        try:
            output = (
                AuxiliaryLLMAudioClient(
                    assistant=msg.multimodal_chat.assistant,
                    chat_object=msg.multimodal_chat).tts_audio_content_message(message=msg)
            )
        except Exception as e:
            return JsonResponse({'audio_url': None})
        try:
            msg.message_audio = output['audio_url']
            msg.save()
        except Exception as e:
            pass
        return JsonResponse({'audio_url': output['audio_url']})
