#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: stream_chat_views.py
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

import base64
import logging

from django.contrib import messages
from django.contrib.auth.models import User

from django.shortcuts import (
    get_object_or_404,
    redirect
)

from django.views import View

from apps.core.generative_ai.generative_ai_decode_manager import (
    GenerativeAIDecodeController
)

from apps.core.media_managers.media_manager_execution_handler import (
    MediaManager
)

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.multimodal_chat.models import (
    MultimodalChat,
    MultimodalChatMessage
)

from apps.user_permissions.utils import (
    PermissionNames
)

logger = logging.getLogger(__name__)


class ChatView_ChatStream(View):
    def post(self, request, *args, **kwargs):
        context_user_id = request.POST.get('user_id')

        context_user = get_object_or_404(
            User,
            id=context_user_id
        )

        ##############################
        # PERMISSION CHECK FOR - CREATE_AND_USE_CHATS
        if not UserPermissionManager.is_authorized(
            user=context_user,
            operation=PermissionNames.CREATE_AND_USE_CHATS
        ):
            messages.error(self.request, "You do not have permission to create and use chats.")

            return redirect('multimodal_chat:chat')
        ##############################

        (
            attached_files,
            attached_images,
            chat,
            message_content,
            sketch_image_full_uris_list
        ) = (
            self._handle_sketch_images(request)
        )

        edit_image_full_uris_list = self._handle_edit_images(
            request
        )

        image_full_uris = self._handle_save_images(
            attached_images,
            edit_image_full_uris_list,
            sketch_image_full_uris_list
        )

        file_full_uris = self._handle_save_files(
            attached_files
        )

        self._handle_record_audio(
            file_full_uris,
            request
        )

        logger.info(f"Chat was streamed by User: {context_user.id}.")

        user_msg = MultimodalChatMessage.objects.create(
            multimodal_chat=chat,
            sender_type='USER',
            message_text_content=message_content,
            message_image_contents=image_full_uris,
            message_file_contents=file_full_uris
        )

        int_llm_c = GenerativeAIDecodeController.get(
            assistant=chat.assistant,
            multimodal_chat=chat
        )

        output = int_llm_c.respond_stream(
            latest_message=user_msg,
            image_uris=image_full_uris,
            file_uris=file_full_uris
        )

        MultimodalChatMessage.objects.create(
            multimodal_chat=chat,
            sender_type='ASSISTANT',
            message_text_content=output
        )

        logger.info(f"Assistant responded to User: {context_user.id}.")
        return redirect('multimodal_chat:chat')

    @staticmethod
    def _handle_record_audio(
        file_full_uris,
        request
    ):
        record_audio = request.POST.get('record_audio')
        audio_full_uri = None

        if record_audio:
            audio_base_64 = request.POST.get('record_audio')

            audio_bytes = base64.b64decode(
                audio_base_64.split("base64,")[1].encode()
            )

            audio_full_uri = MediaManager.save_files_and_return_uris(
                [
                    (
                        audio_bytes,
                        'audio.webm'
                    )
                ]
            )[0]

        if audio_full_uri:
            file_full_uris.append(
                audio_full_uri
            )

    @staticmethod
    def _handle_save_files(
        attached_files
    ):
        file_bytes_list = []
        for file in attached_files:
            file_name = file.name

            try:
                file_bytes = file.read()

                logger.info(f"File: {file_name} was read successfully.")

            except Exception as e:
                logger.error(f"Error while reading file: {file_name}.")
                continue

            file_bytes_list.append(
                (
                    file_bytes,
                    file_name
                )
            )

        file_full_uris = MediaManager.save_files_and_return_uris(
            file_bytes_list
        )

        return file_full_uris

    @staticmethod
    def _handle_sketch_images(request):
        chat_id = request.POST.get('chat_id')

        chat = get_object_or_404(
            MultimodalChat,
            id=chat_id,
            user=request.user
        )

        message_content = request.POST.get('message_content')

        attached_images = request.FILES.getlist('attached_images[]')
        attached_files = request.FILES.getlist('attached_files[]')

        sketch_image = {
            'sketch_image': None
        }

        attached_canvas_image = request.POST.get('sketch_image')
        sketch_image_full_uris_list = []

        try:
            sketch_image_bytes = base64.b64decode(
                attached_canvas_image.split("base64,")[1].encode()
            )

            sketch_image['sketch_image'] = sketch_image_bytes

            sketch_image_full_uris_list = MediaManager.save_sketch(
                sketch_data_map=sketch_image
            )

            logger.info(f"Sketch image was saved successfully.")

        except Exception as e:
            logger.error(f"Error while saving sketch image.")
            pass

        return attached_files, attached_images, chat, message_content, sketch_image_full_uris_list

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

                logger.info(f"Image: {image.name} was read successfully.")

            except Exception as e:
                logger.error(f"Error while reading image: {image.name}.")
                continue

            image_bytes_list.append(
                image_bytes
            )

        image_full_uris = MediaManager.save_images_and_return_uris(
            image_bytes_list
        )

        if sketch_image_full_uris_list:
            image_full_uris.extend(
                sketch_image_full_uris_list
            )

        if edit_image_full_uris_list:
            image_full_uris.extend(
                edit_image_full_uris_list
            )

        return image_full_uris

    @staticmethod
    def _handle_edit_images(request):
        edit_image_bytes_dict = {
            'edit_image': None,
            'edit_image_mask': None
        }

        attached_edit_image = request.FILES.get('edit_image')
        attached_edit_image_mask = request.POST.get('edit_image_mask')

        edit_image_full_uris_list = []

        try:
            edit_image_bytes = attached_edit_image.read()

            edit_image_mask_bytes = base64.b64decode(
                attached_edit_image_mask.split("base64,")[1].encode()
            )

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
