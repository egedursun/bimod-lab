#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: stream_chat_views.py
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
import base64

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from apps._services.llms.llm_decoder import InternalLLMClient
from apps._services.storages.storage_executor import StorageExecutor
from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.multimodal_chat.models import MultimodalChat, MultimodalChatMessage
from apps.user_permissions.utils import PermissionNames


class ChatStreamView(View):
    """
    Handles the streaming of chat messages.

    This view allows users to send messages and attachments to the chat assistant and receive responses in real-time.
    The view also manages the streaming of chat messages and related data.

    Methods:
        post(self, request, *args, **kwargs): Processes the user message and attachment inputs, sends them to the
        chat assistant, and streams the response.
    """

    def post(self, request, *args, **kwargs):
        # 1. Permission check
        context_user_id = request.POST.get('user_id')
        context_user = get_object_or_404(User, id=context_user_id)

        ##############################
        # PERMISSION CHECK FOR - CREATE_AND_USE_CHATS
        if not UserPermissionManager.is_authorized(user=context_user,
                                                   operation=PermissionNames.CREATE_AND_USE_CHATS):
            messages.error(self.request, "You do not have permission to create and use chats.")
            return redirect('multimodal_chat:chat')
        ##############################

        # 2. Content, image, file, and other inputs retrieval
        chat_id = request.POST.get('chat_id')
        chat = get_object_or_404(MultimodalChat, id=chat_id, user=request.user)
        message_content = request.POST.get('message_content')
        attached_images = request.FILES.getlist('attached_images[]')
        attached_files = request.FILES.getlist('attached_files[]')
        print(f"[ChatStreamView.post] The message content has been extracted successfully.")

        sketch_image = {'sketch_image': None}
        attached_canvas_image = request.POST.get('sketch_image')
        sketch_image_full_uris_list = []
        try:
            sketch_image_bytes = base64.b64decode(attached_canvas_image.split("base64,")[1].encode())
            sketch_image['sketch_image'] = sketch_image_bytes
            sketch_image_full_uris_list = StorageExecutor.save_sketch_images(sketch_image_dict=sketch_image)
        except Exception as e:
            # No image attached
            print(f"[ChatStreamView.post] Error while extracting the sketch image: {e}")
            pass
        print(f"[ChatStreamView.post] The sketch image(s) has been extracted successfully.")

        edit_image_bytes_dict = {'edit_image': None, 'edit_image_mask': None}
        attached_edit_image = request.FILES.get('edit_image')
        attached_edit_image_mask = request.POST.get('edit_image_mask')
        edit_image_full_uris_list = []
        try:
            edit_image_bytes = attached_edit_image.read()
            edit_image_mask_bytes = base64.b64decode(attached_edit_image_mask.split("base64,")[1].encode())
            edit_image_bytes_dict['edit_image'] = edit_image_bytes
            edit_image_bytes_dict['edit_image_mask'] = edit_image_mask_bytes
            edit_image_full_uris_list = StorageExecutor.save_edit_images(edit_image_dict=edit_image_bytes_dict)
        except Exception as e:
            # No image attached
            print(f"[ChatStreamView.post] Error while extracting the edit image: {e}")
            pass
        print(f"[ChatStreamView.post] The edit image(s) has been extracted successfully.")

        # 3. Handle the file and image uploads
        image_bytes_list = []
        for image in attached_images:
            try:
                image_bytes = image.read()
            except Exception as e:
                print(f"[ChatView.post] Error reading image file: {e}")
                continue
            image_bytes_list.append(image_bytes)
        image_full_uris = StorageExecutor.save_images_and_provide_full_uris(image_bytes_list)
        if sketch_image_full_uris_list:
            image_full_uris.extend(sketch_image_full_uris_list)
        if edit_image_full_uris_list:
            image_full_uris.extend(edit_image_full_uris_list)
        print(f"[ChatStreamView.post] The image(s) has been uploaded successfully.")

        file_bytes_list = []
        for file in attached_files:
            file_name = file.name
            try:
                file_bytes = file.read()
            except Exception as e:
                print(f"[ChatView.post] Error reading file: {e}")
                continue
            file_bytes_list.append((file_bytes, file_name))
        file_full_uris = StorageExecutor.save_files_and_provide_full_uris(file_bytes_list)
        print(f"[ChatStreamView.post] The file(s) has been uploaded successfully.")

        record_audio = request.POST.get('record_audio')
        audio_full_uri = None
        if record_audio:
            audio_base_64 = request.POST.get('record_audio')
            audio_bytes = base64.b64decode(audio_base_64.split("base64,")[1].encode())
            audio_full_uri = StorageExecutor.save_files_and_provide_full_uris([(audio_bytes, 'audio.webm')])[0]
            print(f"[ChatStreamView.post] The audio file has been uploaded successfully.")
        if audio_full_uri:
            file_full_uris.append(audio_full_uri)
            print(f"[ChatStreamView.post] The audio file has been added to the file URIs list: {file_full_uris}")

        # 4. Create the user message
        MultimodalChatMessage.objects.create(
            multimodal_chat=chat, sender_type='USER', message_text_content=message_content,
            message_image_contents=image_full_uris, message_file_contents=file_full_uris
        )
        user_message = MultimodalChatMessage.objects.filter(multimodal_chat=chat).last()
        print(f"[ChatStreamView.post] The user message has been created successfully.")
        print(f"[ChatStreamView.post] User message: {user_message}")
        print(f"[ChatStreamView.post] User message content: {user_message.message_text_content}")

        internal_llm_client = InternalLLMClient.get(assistant=chat.assistant, multimodal_chat=chat)
        print(f"[ChatStreamView.post] Calling the 'handle_streaming' function...")
        final_response = internal_llm_client.respond_stream(latest_message=user_message, image_uris=image_full_uris,
                                                            file_uris=file_full_uris)
        MultimodalChatMessage.objects.create(
            multimodal_chat=chat, sender_type='ASSISTANT', message_text_content=final_response)

        print(f"[ChatStreamView.post] Calling the 'streamer' function of OpenAI to stream the response...")
        return redirect('multimodal_chat:chat')
