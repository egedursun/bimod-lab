from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from web_project import TemplateLayout, TemplateHelper
from .models import MultimodalChat, MultimodalChatMessage
from .utils import generate_chat_name
from ..assistants.models import Assistant
from ..user_permissions.models import UserPermission, PermissionNames


class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'multimodal_chat/chat.html'

    def get_context_data(self, **kwargs):
        active_chat = None
        if 'chat_id' in self.request.GET:
            active_chat = get_object_or_404(MultimodalChat, id=self.request.GET['chat_id'], user=self.request.user)
        chats = MultimodalChat.objects.filter(user=self.request.user)

        # if there is an active chat, put the active chat at the beginning of the list
        if active_chat:
            chats = [active_chat] + [chat for chat in chats if chat.id != active_chat.id]

        assistants = Assistant.objects.filter(organization__users=self.request.user)

        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        active_chat_messages = active_chat.chat_messages.all().order_by('sent_at') if active_chat else None
        context.update(
            {
                "chats": chats,
                "assistants": assistants,
                "active_chat": active_chat,
                "chat_messages": active_chat_messages
            }
        )
        return context

    def post(self, request, *args, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - LLM/CREATE
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
                created_by_user=request.user
            )
            active_chat = chat
        elif 'new_chat_name' in request.POST:
            chat_id = request.POST.get('chat_id')
            chat = get_object_or_404(MultimodalChat, id=chat_id, user=request.user)
            chat.chat_name = request.POST.get('new_chat_name')
            chat.save()
            active_chat = chat
        else:
            chat_id = request.POST.get('chat_id')
            chat = get_object_or_404(MultimodalChat, id=chat_id, user=request.user)
            message_content = request.POST.get('message_content')
            MultimodalChatMessage.objects.create(
                multimodal_chat=chat,
                sender_type='USER',
                message_text_content=message_content
            )
            active_chat = chat

            # redirect with '?chat_id=' to keep the chat open
            redirect_string = self.request.path_info + '?chat_id=' + str(active_chat.id)
            return redirect(redirect_string, *args, **kwargs)

        chats = MultimodalChat.objects.filter(user=request.user)
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

        return render(request, self.template_name, context)


class ChatDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'multimodal_chat/confirm_delete_chat.html'
    success_url = '/chat/'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        chat = self.get_object()
        context['chat'] = chat
        return context


    def get_queryset(self):
        return MultimodalChat.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        chat = get_object_or_404(MultimodalChat, id=self.kwargs['pk'], user=self.request.user)
        chat.delete()
        return redirect('multimodal_chat:chat')

