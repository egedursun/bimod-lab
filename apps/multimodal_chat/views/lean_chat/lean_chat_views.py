#  Copyright Policy & Ownership
#
#  Bimod.io is a product of BMD Holdings. All materials, including but not limited to software, code, documentation,
#  graphics, design elements, and user interfaces provided by Bimod.io are protected by copyright law and international
#  treaties.
#  All content within Bimod.io is the exclusive property of BMD Holdings, unless otherwise stated.
#  Unauthorized use, distribution, or reproduction of any material contained in this software without the express
#  written consent of BMD Holdings is strictly prohibited.
#  Users may not copy, modify, distribute, display, perform, or create derivative works of Bimod.io without prior
#  written permission from BMD Holdings.
import base64

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView

from apps._services.storages.storage_executor import StorageExecutor
from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.leanmod.models import LeanAssistant
from apps.message_templates.models import MessageTemplate
from apps.multimodal_chat.models import MultimodalLeanChat, MultimodalLeanChatMessage
from apps.multimodal_chat.utils import ChatSourcesNames, generate_chat_name
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from config.settings import MEDIA_URL
from web_project import TemplateLayout, TemplateHelper


class LeanChatView(TemplateView, LoginRequiredMixin):

    @staticmethod
    def refresh_page(chat_id, user_id):
        print(f"[LeanChatView.refresh_page] Refreshing page with new response...")
        print(f"[LeanChatView.refresh_page] Chat ID: {chat_id}")
        print(f"[LeanChatView.refresh_page] User ID: {user_id}")
        try:
            print(f"[LeanChatView.refresh_page] Successfully added new response to chat {chat_id}")
        except Exception as e:
            print(f"[LeanChatView.refresh_page] Error while refreshing page with new response: {e}")

        # refresh the page with the new response
        return redirect(f'/lean_chat/?chat_id={chat_id}')

    def get_context_data(self, **kwargs):
        active_chat = None
        context_user = self.request.user
        if 'chat_id' in self.request.GET:
            active_chat = get_object_or_404(MultimodalLeanChat, id=self.request.GET['chat_id'], user=self.request.user)
        chats = MultimodalLeanChat.objects.filter(
            user=self.request.user, chat_source=ChatSourcesNames.APP, is_archived=False
        )
        # if there is an active chat, put the active chat at the beginning of the list
        if active_chat:
            chats = [active_chat] + [chat for chat in chats if chat.id != active_chat.id]
        else:
            # Do NOT put an active chat directly
            pass

        lean_assistants = LeanAssistant.objects.filter(organization__users=self.request.user)
        organizations = Organization.objects.filter(lean_assistants__in=lean_assistants)
        message_templates = MessageTemplate.objects.filter(user=context_user, organization__in=organizations)
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        active_chat_messages = active_chat.lean_chat_messages.all().order_by('sent_at') if active_chat else None
        context.update(
            {
                "chats": chats, "assistants": lean_assistants, "active_chat": active_chat,
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
        # PERMISSION CHECK FOR - CREATE_AND_USE_LEAN_CHATS
        if not UserPermissionManager.is_authorized(user=context_user,
                                                   operation=PermissionNames.CREATE_AND_USE_LEAN_CHATS):
            messages.error(self.request, "You do not have permission to create and use LeanMod chats.")
            return redirect('multimodal_chat:lean_chat')
        ##############################

        if 'assistant_id' in request.POST:
            assistant_id = request.POST.get('assistant_id')
            assistant = get_object_or_404(LeanAssistant, id=assistant_id, organization__users=request.user)
            chat = MultimodalLeanChat.objects.create(
                organization=assistant.organization, lean_assistant=assistant, user=request.user,
                chat_name=request.POST.get('chat_name', generate_chat_name()), created_by_user=request.user,
                chat_source=ChatSourcesNames.APP
            )
            active_chat = chat
        elif 'new_chat_name' in request.POST:
            chat_id = request.POST.get('chat_id')
            chat = get_object_or_404(MultimodalLeanChat, id=chat_id, user=request.user)
            chat.chat_name = request.POST.get('new_chat_name')
            chat.save()
            active_chat = chat
            """
            INFO: No starred message for LeanMod chats yet.
            """
        else:
            chat_id = request.POST.get('chat_id')
            chat = get_object_or_404(MultimodalLeanChat, id=chat_id, user=request.user)
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
                # No image attached
                print(f"[LeanChatView.post] Error while extracting the sketch image: {e}")
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
                print(f"[LeanChatView.post] Error while extracting the edit image mask: {e}")
                pass

            # Upload the attached images
            image_bytes_list = []
            for image in attached_images:
                try:
                    image_bytes = image.read()
                except Exception as e:
                    print(f"[LeanChatView.post] Error reading image file: {e}")
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
                    print(f"[LeanChatView.post] Error reading file: {e}")
                    continue
                file_bytes_list.append((file_bytes, file_name))
            file_full_uris = StorageExecutor.save_files_and_provide_full_uris(file_bytes_list)

            record_audio = request.POST.get('record_audio')
            audio_full_uri = None
            if record_audio:
                audio_base_64 = request.POST.get('record_audio')
                audio_bytes = base64.b64decode(audio_base_64.split("base64,")[1].encode())
                audio_full_uri = StorageExecutor.save_files_and_provide_full_uris([(audio_bytes, 'audio.webm')])[0]
                print(f"[LeanChatView.post] The audio file has been uploaded successfully.")
            if audio_full_uri:
                file_full_uris.append(audio_full_uri)
                print(f"[LeanChatView.post] The audio file has been added to the file URIs list: {file_full_uris}")

            MultimodalLeanChatMessage.objects.create(
                multimodal_lean_chat=chat, sender_type='USER', message_text_content=message_content,
                message_image_contents=image_full_uris, message_file_contents=file_full_uris
            )
            user_message = MultimodalLeanChatMessage.objects.filter(multimodal_lean_chat=chat).last()
            internal_llm_client_lean = InternalLLMClient.get_lean(assistant=chat.lean_assistant, multimodal_chat=chat)
            response = internal_llm_client_lean.respond(latest_message=user_message,
                                                        image_uris=image_full_uris,
                                                        file_uris=file_full_uris)
            MultimodalLeanChatMessage.objects.create(
                multimodal_lean_chat=chat, sender_type='ASSISTANT', message_text_content=response
            )
            active_chat = chat
        chats = MultimodalLeanChat.objects.filter(user=request.user, chat_source=ChatSourcesNames.APP)
        lean_assistants = LeanAssistant.objects.filter(organization__users=request.user)
        context.update(
            {
                "layout_path": TemplateHelper.set_layout("layout_vertical.html", context),
                'chat_id': active_chat.id if active_chat else None, 'chats': chats, 'assistants': lean_assistants,
                'active_chat': active_chat
            }
        )
        redirect_string = self.request.path_info + '?chat_id=' + str(active_chat.id)
        return redirect(redirect_string, *args, **kwargs)
