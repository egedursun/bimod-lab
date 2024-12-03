#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from apps.core.generative_ai.auxiliary_clients.auxiliary_llm_audio_client import (
    AuxiliaryLLMAudioClient
)

from apps.multimodal_chat.models import (
    MultimodalChatMessage,
    MultimodalLeanChatMessage
)

from apps.voidforger.models import MultimodalVoidForgerChatMessage

logger = logging.getLogger(__name__)


class Chat_MessageNarration(LoginRequiredMixin, View):
    def get(
        self,
        request,
        *args,
        **kwargs
    ):

        msg_id = kwargs.get('pk')

        try:
            msg = get_object_or_404(
                MultimodalChatMessage,
                id=msg_id,
                multimodal_chat__user=request.user
            )

        except Exception as e:
            logger.error(f"Assistant chat message not found. Error: {e}")
            return JsonResponse({'audio_url': None})

        try:
            if msg.message_audio:
                logger.info(f"Assistant chat message audio found. Returning audio URL.")
                return JsonResponse({'audio_url': msg.message_audio})

        except Exception as e:
            logger.error(f"Assistant chat message audio not found. Error: {e}")
            pass

        try:
            output = (
                AuxiliaryLLMAudioClient(
                    assistant=msg.multimodal_chat.assistant,
                    chat_object=msg.multimodal_chat
                ).tts_audio_content_message(
                    message=msg
                )
            )

        except Exception as e:
            logger.error(f"Assistant chat message audio generation failed. Error: {e}")
            return JsonResponse({'audio_url': None})

        try:
            msg.message_audio = output['audio_url']
            msg.save()

            logger.info(f"Assistant chat message audio generated and saved.")

        except Exception as e:
            logger.error(f"Assistant chat message audio saving failed. Error: {e}")
            pass

        logger.info(f"Assistant chat message audio generated. Returning audio URL.")
        return JsonResponse({'audio_url': output['audio_url']})


class LeanChat_MessageNarration(LoginRequiredMixin, View):
    def get(
        self,
        request,
        *args,
        **kwargs
    ):

        msg_id = kwargs.get('pk')

        try:
            msg = get_object_or_404(
                MultimodalLeanChatMessage,
                id=msg_id,
                multimodal_lean_chat__user=request.user
            )

        except Exception as e:
            logger.error(f"LeanMod chat message not found. Error: {e}")
            return JsonResponse({'audio_url': None})

        try:
            if msg.message_audio:
                logger.info(f"LeanMod chat message audio found. Returning audio URL.")
                return JsonResponse({'audio_url': msg.message_audio})

        except Exception as e:
            logger.error(f"LeanMod chat message audio not found. Error: {e}")
            pass

        try:
            output = (
                AuxiliaryLLMAudioClient(
                    assistant=msg.multimodal_lean_chat.lean_assistant,
                    chat_object=msg.multimodal_lean_chat
                ).tts_audio_content_message(
                    message=msg
                )
            )

        except Exception as e:
            logger.error(f"LeanMod chat message audio generation failed. Error: {e}")
            return JsonResponse({'audio_url': None})

        try:
            msg.message_audio = output['audio_url']
            msg.save()

            logger.info(f"LeanMod chat message audio generated and saved.")

        except Exception as e:
            logger.error(f"LeanMod chat message audio saving failed. Error: {e}")
            pass

        logger.info(f"LeanMod chat message audio generated. Returning audio URL.")
        return JsonResponse({'audio_url': output['audio_url']})


class VoidForgerChat_MessageNarration(LoginRequiredMixin, View):
    def get(
        self,
        request,
        *args,
        **kwargs
    ):

        msg_id = kwargs.get('pk')

        try:
            msg = get_object_or_404(
                MultimodalVoidForgerChatMessage,
                id=msg_id,
                multimodal_voidforger_chat__user=request.user
            )

        except Exception as e:
            logger.error(f"VoidForger chat message not found. Error: {e}")
            return JsonResponse({'audio_url': None})

        try:

            if msg.message_audio:
                logger.info(f"VoidForger chat message audio found. Returning audio URL.")
                return JsonResponse({'audio_url': msg.message_audio})

        except Exception as e:
            logger.error(f"VoidForger chat message audio not found. Error: {e}")
            pass

        try:
            output = (
                AuxiliaryLLMAudioClient(
                    assistant=msg.multimodal_voidforger_chat.voidforger,
                    chat_object=msg.multimodal_voidforger_chat
                ).tts_audio_content_message(
                    message=msg
                )
            )

        except Exception as e:
            logger.error(f"VoidForger chat message audio generation failed. Error: {e}")
            return JsonResponse({'audio_url': None})

        try:
            msg.message_audio = output['audio_url']
            msg.save()

            logger.info(f"VoidForger chat message audio generated and saved.")

        except Exception as e:
            logger.error(f"VoidForger chat message audio saving failed. Error: {e}")
            pass

        logger.info(f"VoidForger chat message audio generated. Returning audio URL.")
        return JsonResponse({'audio_url': output['audio_url']})
