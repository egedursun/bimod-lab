#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: chat_views.py
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
#  File: chat_views.py
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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView

from apps._services.storages.storage_executor import StorageExecutor
from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.message_templates.models import MessageTemplate
from apps.multimodal_chat.models import MultimodalChat, MultimodalChatMessage
from apps.multimodal_chat.utils import ChatSourcesNames, generate_chat_name
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from config.settings import MEDIA_URL
from web_project import TemplateLayout, TemplateHelper


class ChatView(LoginRequiredMixin, TemplateView):
    """
    Handles the creation, management, and display of multimodal chats.

    This view allows users to create new chats, rename existing chats, star messages, and send messages with various
    attachments. It also manages the display of chat messages and related templates.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with the active chat, messages, assistants, and message
        templates.
        post(self, request, *args, **kwargs): Processes the creation and management of chats, including sending
        messages and attachments.
    """

    template_name = 'multimodal_chat/chats/chat.html'

    @staticmethod
    def refresh_page(chat_id, user_id):
        print(f"[ChatView.refresh_page] Refreshing page with new response...")
        print(f"[ChatView.refresh_page] Chat ID: {chat_id}")
        print(f"[ChatView.refresh_page] User ID: {user_id}")
        try:
            print(f"[ChatView.refresh_page] Successfully added new response to chat {chat_id}")
        except Exception as e:
            print(f"[ChatView.refresh_page] Error while refreshing page with new response: {e}")

        # refresh the page with the new response
        return redirect(f'/chat/?chat_id={chat_id}')

    def get_context_data(self, **kwargs):
        active_chat = None
        context_user = self.request.user
        if 'chat_id' in self.request.GET:
            active_chat = get_object_or_404(MultimodalChat, id=self.request.GET['chat_id'], user=self.request.user)
        chats = MultimodalChat.objects.filter(
            user=self.request.user, chat_source=ChatSourcesNames.APP, is_archived=False
        )
        # if there is an active chat, put the active chat at the beginning of the list
        if active_chat:
            chats = [active_chat] + [chat for chat in chats if chat.id != active_chat.id]
        else:
            # Do NOT put an active chat directly
            pass

        assistants = Assistant.objects.filter(organization__users=self.request.user)
        organizations = Organization.objects.filter(assistants__in=assistants)
        message_templates = MessageTemplate.objects.filter(user=context_user, organization__in=organizations)
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        active_chat_messages = active_chat.chat_messages.all().order_by('sent_at') if active_chat else None
        context.update(
            {
                "chats": chats, "assistants": assistants, "active_chat": active_chat,
                "user": context_user,
                "chat_messages": active_chat_messages, "message_templates": message_templates, "base_url": MEDIA_URL
            }
        )
        return context

    def post(self, request, *args, **kwargs):
        from apps._services.llms.llm_decoder import InternalLLMClient
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - CREATE_AND_USE_CHATS
        if not UserPermissionManager.is_authorized(user=context_user,
                                                   operation=PermissionNames.CREATE_AND_USE_CHATS):
            messages.error(self.request, "You do not have permission to create and use chats.")
            return redirect('multimodal_chat:chat')
        ##############################

        if 'assistant_id' in request.POST:
            assistant_id = request.POST.get('assistant_id')
            assistant = get_object_or_404(Assistant, id=assistant_id, organization__users=request.user)
            chat = MultimodalChat.objects.create(
                organization=assistant.organization, assistant=assistant, user=request.user,
                chat_name=request.POST.get('chat_name', generate_chat_name()), created_by_user=request.user,
                chat_source=ChatSourcesNames.APP
            )
            active_chat = chat
        elif 'new_chat_name' in request.POST:
            chat_id = request.POST.get('chat_id')
            chat = get_object_or_404(MultimodalChat, id=chat_id, user=request.user)
            chat.chat_name = request.POST.get('new_chat_name')
            chat.save()
            active_chat = chat
        elif 'starred_message' in request.POST:
            chat_id = request.POST.get('chat_id')
            chat = get_object_or_404(MultimodalChat, id=chat_id, user=request.user)
            message_id = request.POST.get('message_id')
            message = get_object_or_404(MultimodalChatMessage, id=message_id, multimodal_chat=chat)
            message.starred = not message.starred
            message.save()
            active_chat = chat
        else:
            chat_id = request.POST.get('chat_id')
            chat = get_object_or_404(MultimodalChat, id=chat_id, user=request.user)
            message_content = request.POST.get('message_content')
            attached_images = request.FILES.getlist('attached_images[]')
            attached_files = request.FILES.getlist('attached_files[]')
            # canvas image
            sketch_image = {'sketch_image': None}
            attached_canvas_image = request.POST.get('sketch_image')
            sketch_image_full_uris_list = []
            try:
                sketch_image_bytes = base64.b64decode(attached_canvas_image.split("base64,")[1].encode())
                sketch_image['sketch_image'] = sketch_image_bytes
                sketch_image_full_uris_list = StorageExecutor.save_sketch_images(sketch_image_dict=sketch_image)
            except Exception as e:
                print(f"[ChatView.post] Error while extracting the sketch image: {e}")
                # No image attached
                pass

            # image modification
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
                print(f"[ChatView.post] Error while extracting the edit image mask: {e}")
                pass

            # Upload the attached images
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
            # Upload the attached files
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

            record_audio = request.POST.get('record_audio')
            audio_full_uri = None
            if record_audio:
                audio_base_64 = request.POST.get('record_audio')
                audio_bytes = base64.b64decode(audio_base_64.split("base64,")[1].encode())
                audio_full_uri = StorageExecutor.save_files_and_provide_full_uris([(audio_bytes, 'audio.webm')])[0]
                print(f"[ChatView.post] The audio file has been uploaded successfully.")
            if audio_full_uri:
                file_full_uris.append(audio_full_uri)
                print(f"[ChatView.post] The audio file has been added to the file URIs list: {file_full_uris}")

            MultimodalChatMessage.objects.create(
                multimodal_chat=chat, sender_type='USER', message_text_content=message_content,
                message_image_contents=image_full_uris, message_file_contents=file_full_uris
            )
            user_message = MultimodalChatMessage.objects.filter(multimodal_chat=chat).last()
            internal_llm_client = InternalLLMClient.get(assistant=chat.assistant, multimodal_chat=chat)
            response = internal_llm_client.respond(latest_message=user_message,
                                                   image_uris=image_full_uris,
                                                   file_uris=file_full_uris)
            MultimodalChatMessage.objects.create(
                multimodal_chat=chat, sender_type='ASSISTANT', message_text_content=response
            )
            active_chat = chat
        chats = MultimodalChat.objects.filter(user=request.user, chat_source=ChatSourcesNames.APP)
        assistants = Assistant.objects.filter(organization__users=request.user)
        context.update(
            {
                "layout_path": TemplateHelper.set_layout("layout_vertical.html", context),
                'chat_id': active_chat.id if active_chat else None, 'chats': chats, 'assistants': assistants,
                'active_chat': active_chat
            }
        )
        redirect_string = self.request.path_info + '?chat_id=' + str(active_chat.id)
        return redirect(redirect_string, *args, **kwargs)
