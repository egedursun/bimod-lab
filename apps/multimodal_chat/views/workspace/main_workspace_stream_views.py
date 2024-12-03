#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: main_workspace_stream_views.py
#  Last Modified: 2024-11-16 05:07:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-16 05:07:09
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import base64
import logging

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from apps.core.generative_ai.generative_ai_decode_manager import (
    GenerativeAIDecodeController
)

from apps.core.media_managers.media_manager_execution_handler import (
    MediaManager
)

from apps.core.tool_calls.utils import (
    VoidForgerModesNames
)

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.user_permissions.utils import (
    PermissionNames
)

from apps.voidforger.models import (
    MultimodalVoidForgerChat,
    MultimodalVoidForgerChatMessage
)

logger = logging.getLogger(__name__)


class ChatView_MainWorkspaceStream(View):

    def post(self, request, *args, **kwargs):
        context_user_id = request.POST.get('user_id')
        context_user = get_object_or_404(User, id=context_user_id)

        ##############################
        # PERMISSION CHECK FOR - CREATE_AND_USE_VOIDFORGER_CHATS
        if not UserPermissionManager.is_authorized(
            user=context_user,
            operation=PermissionNames.CREATE_AND_USE_VOIDFORGER_CHATS
        ):
            messages.error(self.request, "You do not have permission to create and use VoidForger chats.")
            return redirect('multimodal_chat:main_workspace')
        ##############################

        chat_id = request.POST.get('chat_id')

        chat: MultimodalVoidForgerChat = get_object_or_404(
            MultimodalVoidForgerChat,
            id=chat_id,
            user=request.user
        )

        msg_content = request.POST.get('message_content')
        attached_images = request.FILES.getlist('attached_images[]')
        attached_files = request.FILES.getlist('attached_files[]')

        sketch_image_full_uris_list = self._handle_sketch_image(request)
        edit_image_full_uris_list = self._handle_edit_image(request)

        image_full_uris = self._handle_save_images(
            attached_images,
            edit_image_full_uris_list,
            sketch_image_full_uris_list
        )

        file_full_uris = self._handle_save_files(attached_files)
        self._handle_record_audio(file_full_uris, request)

        try:
            MultimodalVoidForgerChatMessage.objects.create(
                multimodal_voidforger_chat=chat,
                sender_type='USER',
                message_text_content=msg_content,
                message_image_contents=image_full_uris,
                message_file_contents=file_full_uris
            )

            logger.info(f"User message was saved successfully.")

        except Exception as e:
            logger.error(f"Error while saving User message.")
            messages.error(self.request, "Error while saving User message: " + str(e))
            return redirect('multimodal_chat:main_workspace')

        try:
            user_msg = MultimodalVoidForgerChatMessage.objects.filter(
                multimodal_voidforger_chat=chat
            ).last()

            internal_llm_client_voidforger = GenerativeAIDecodeController.get_voidforger(
                user=request.user,
                assistant=chat.voidforger,
                multimodal_chat=chat
            )

            final_response = internal_llm_client_voidforger.respond_stream(
                latest_message=user_msg,
                current_mode=VoidForgerModesNames.CHAT,
                image_uris=image_full_uris,
                file_uris=file_full_uris
            )

        except Exception as e:
            logger.error(f"Error while responding to User: {context_user.id}.")
            messages.error(self.request, "Error while responding: " + str(e))

            return redirect('multimodal_chat:main_workspace')

        MultimodalVoidForgerChatMessage.objects.create(
            multimodal_voidforger_chat=chat,
            sender_type='ASSISTANT',
            message_text_content=final_response
        )

        logger.info(f"VoidForger responded to User: {context_user.id}.")
        return redirect('multimodal_chat:main_workspace')

    @staticmethod
    def _handle_record_audio(
        file_full_uris,
        request
    ):

        record_audio = request.POST.get('record_audio')
        audio_full_uri = None

        if record_audio:
            audio_base_64 = request.POST.get('record_audio')
            audio_bytes = base64.b64decode(audio_base_64.split("base64,")[1].encode())
            audio_full_uri = MediaManager.save_files_and_return_uris([(audio_bytes, 'audio.webm')])[0]

        if audio_full_uri:
            file_full_uris.append(audio_full_uri)

        logger.info(f"Audio was saved successfully.")
        return

    @staticmethod
    def _handle_save_files(attached_files):
        file_bytes_list = []

        for file in attached_files:
            file_name = file.name

            try:
                file_bytes = file.read()
                logger.info(f"File was read successfully.")

            except Exception as e:
                logger.error(f"Error while reading file.")
                continue

            file_bytes_list.append((file_bytes, file_name))

        file_full_uris = MediaManager.save_files_and_return_uris(file_bytes_list)
        return file_full_uris

    @staticmethod
    def _handle_save_images(
        attached_images,
        edit_image_full_uris_list,
        sketch_image_full_uris_list
    ):

        image_bytes_list = []

        for image in attached_images:

            try:
                image_bytes = image.read()
                logger.info(f"Image was read successfully.")

            except Exception as e:
                logger.error(f"Error while reading image.")
                continue

            image_bytes_list.append(image_bytes)

        image_full_uris = MediaManager.save_images_and_return_uris(image_bytes_list)

        if sketch_image_full_uris_list:
            image_full_uris.extend(sketch_image_full_uris_list)

        if edit_image_full_uris_list:
            image_full_uris.extend(edit_image_full_uris_list)

        return image_full_uris

    @staticmethod
    def _handle_edit_image(request):
        edit_image_bytes_dict = {
            'edit_image': None,
            'edit_image_mask': None
        }

        attached_edit_image = request.FILES.get('edit_image')
        attached_edit_image_mask = request.POST.get('edit_image_mask')
        edit_image_full_uris_list = []

        try:
            edit_image_bytes = attached_edit_image.read()
            edit_image_mask_bytes = base64.b64decode(attached_edit_image_mask.split("base64,")[1].encode())

            edit_image_bytes_dict['edit_image'] = edit_image_bytes
            edit_image_bytes_dict['edit_image_mask'] = edit_image_mask_bytes

            edit_image_full_uris_list = MediaManager.save_edit_image_and_masked_image(
                edit_img_map=edit_image_bytes_dict
            )

            logger.info(f"Edit image was saved successfully.")

        except Exception as e:
            logger.error(f"Error while saving edit image.")
            pass

        return edit_image_full_uris_list

    @staticmethod
    def _handle_sketch_image(request):
        sketch_image = {
            'sketch_image': None
        }

        attached_canvas_image = request.POST.get('sketch_image')
        sketch_image_full_uris_list = []

        try:
            sketch_image_bytes = base64.b64decode(attached_canvas_image.split("base64,")[1].encode())
            sketch_image['sketch_image'] = sketch_image_bytes

            sketch_image_full_uris_list = MediaManager.save_sketch(
                sketch_data_map=sketch_image
            )

            logger.info(f"Sketch image was saved successfully.")

        except Exception as e:
            logger.error(f"Error while saving sketch image.")
            pass

        return sketch_image_full_uris_list
