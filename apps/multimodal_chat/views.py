import base64

from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from config.settings import BASE_URL
from web_project import TemplateLayout, TemplateHelper
from .models import MultimodalChat, MultimodalChatMessage, ChatSourcesNames
from .utils import generate_chat_name
from .._services.storages.storage_executor import StorageExecutor
from ..assistants.models import Assistant
from ..datasource_media_storages.models import DataSourceMediaStorageItem
from ..message_templates.models import MessageTemplate
from ..organization.models import Organization
from ..user_permissions.models import UserPermission, PermissionNames


class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'multimodal_chat/chat.html'

    def get_context_data(self, **kwargs):
        active_chat = None
        context_user = self.request.user

        if 'chat_id' in self.request.GET:
            active_chat = get_object_or_404(MultimodalChat, id=self.request.GET['chat_id'], user=self.request.user)

        chats = MultimodalChat.objects.filter(
            user=self.request.user,
            chat_source=ChatSourcesNames.APP,
            is_archived=False
        )

        # if there is an active chat, put the active chat at the beginning of the list
        if active_chat:
            chats = [active_chat] + [chat for chat in chats if chat.id != active_chat.id]
        else:
            if len(chats) > 0:
                active_chat = chats[0]

        assistants = Assistant.objects.filter(organization__users=self.request.user)
        organizations = Organization.objects.filter(
            organization_assistants__in=assistants
        )
        message_templates = MessageTemplate.objects.filter(
            user=context_user,
            organization__in=organizations
        )

        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        active_chat_messages = active_chat.chat_messages.all().order_by('sent_at') if active_chat else None
        context.update(
            {
                "chats": chats,
                "assistants": assistants,
                "active_chat": active_chat,
                "chat_messages": active_chat_messages,
                "message_templates": message_templates,
                "base_url": BASE_URL
            }
        )
        return context

    def post(self, request, *args, **kwargs):
        from .._services.llms.llm_decoder import InternalLLMClient
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - CHAT / CREATE AND USE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.CREATE_AND_USE_CHATS not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {"Permission Error": "You do not have permission to create and use chats."}
            return self.render_to_response(context)
        ##############################

        if 'assistant_id' in request.POST:
            assistant_id = request.POST.get('assistant_id')
            assistant = get_object_or_404(Assistant, id=assistant_id, organization__users=request.user)
            chat = MultimodalChat.objects.create(
                organization=assistant.organization,
                assistant=assistant,
                user=request.user,
                chat_name=request.POST.get('chat_name', generate_chat_name()),
                created_by_user=request.user,
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
                print(f"Error in 'edit image' or 'edit image mask' file: {e}")

            # Upload the attached images
            image_bytes_list = []
            for image in attached_images:
                try:
                    image_bytes = image.read()
                except Exception as e:
                    print(f"Error reading image file: {e}")
                    continue
                image_bytes_list.append(image_bytes)
            image_full_uris = StorageExecutor.save_images_and_provide_full_uris(image_bytes_list)
            if edit_image_full_uris_list:
                image_full_uris.extend(edit_image_full_uris_list)

            # Upload the attached files
            file_bytes_list = []
            for file in attached_files:
                file_name = file.name
                try:
                    file_bytes = file.read()
                except Exception as e:
                    print(f"Error reading file: {e}")
                    continue
                file_bytes_list.append((file_bytes, file_name))
            file_full_uris = StorageExecutor.save_files_and_provide_full_uris(file_bytes_list)

            MultimodalChatMessage.objects.create(
                multimodal_chat=chat,
                sender_type='USER',
                message_text_content=message_content,
                message_image_contents=image_full_uris,
                message_file_contents=file_full_uris
            )
            user_message = MultimodalChatMessage.objects.filter(multimodal_chat=chat).last()
            internal_llm_client = InternalLLMClient.get(assistant=chat.assistant, multimodal_chat=chat)
            response = internal_llm_client.respond(latest_message=user_message,
                                                   image_uris=image_full_uris,
                                                   file_uris=file_full_uris)
            MultimodalChatMessage.objects.create(
                multimodal_chat=chat,
                sender_type='ASSISTANT',
                message_text_content=response
            )

            active_chat = chat

        chats = MultimodalChat.objects.filter(user=request.user, chat_source=ChatSourcesNames.APP)
        assistants = Assistant.objects.filter(organization__users=request.user)

        context.update(
            {
                "layout_path": TemplateHelper.set_layout("layout_vertical.html", context),
                'chat_id': active_chat.id if active_chat else None,
                'chats': chats,
                'assistants': assistants,
                'active_chat': active_chat
            }
        )

        redirect_string = self.request.path_info + '?chat_id=' + str(active_chat.id)
        return redirect(redirect_string, *args, **kwargs)


class ChatDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'multimodal_chat/confirm_delete_chat.html'
    success_url = '/chat/'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        chat = self.get_object()
        context['chat'] = chat
        return context

    def get_queryset(self):
        return MultimodalChat.objects.filter(user=self.request.user, chat_source=ChatSourcesNames.APP)

    def post(self, request, *args, **kwargs):
        chat = get_object_or_404(MultimodalChat, id=self.kwargs['pk'], user=self.request.user)
        chat.delete()
        return redirect('multimodal_chat:chat')


class ChatArchiveView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - CHAT / ARCHIVE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.CREATE_AND_USE_CHATS not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {"Permission Error": "You do not have permission to archive chats."}
            return self.render_to_response(context)
        ##############################

        pk = kwargs.get('pk')
        chat = get_object_or_404(MultimodalChat, id=pk, user=self.request.user)
        chat.is_archived = True
        chat.save()

        return redirect('multimodal_chat:chat')


class ChatUnarchiveView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - CHAT / ARCHIVE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.CREATE_AND_USE_CHATS not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {"Permission Error": "You do not have permission to archive chats."}
            return self.render_to_response(context)
        ##############################

        pk = kwargs.get('pk')
        chat = get_object_or_404(MultimodalChat, id=pk, user=self.request.user)
        chat.is_archived = False
        chat.save()

        return redirect('multimodal_chat:chat')


class ChatArchiveListView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        active_chat = None
        context_user = self.request.user

        if 'chat_id' in self.request.GET:
            active_chat = get_object_or_404(MultimodalChat, id=self.request.GET['chat_id'], user=self.request.user)

        chats = MultimodalChat.objects.filter(
            user=self.request.user,
            chat_source=ChatSourcesNames.APP,
            # Only show the archived chats
            is_archived=True
        )

        # if there is an active chat, put the active chat at the beginning of the list
        if active_chat:
            chats = [active_chat] + [chat for chat in chats if chat.id != active_chat.id]
        else:
            if len(chats) > 0:
                active_chat = chats[0]

        assistants = Assistant.objects.filter(organization__users=self.request.user)
        organizations = Organization.objects.filter(
            organization_assistants__in=assistants
        )
        message_templates = MessageTemplate.objects.filter(
            user=context_user,
            organization__in=organizations
        )

        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        active_chat_messages = active_chat.chat_messages.all().order_by('sent_at') if active_chat else None
        context.update(
            {
                "chats": chats,
                "assistants": assistants,
                "active_chat": active_chat,
                "chat_messages": active_chat_messages,
                "message_templates": message_templates,
                "base_url": BASE_URL
            }
        )
        return context
