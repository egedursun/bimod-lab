from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, DeleteView

from apps.starred_messages.models import StarredMessage
from apps.user_permissions.models import UserPermission, PermissionNames
from config.settings import MEDIA_URL
from web_project import TemplateLayout


class ListStarredMessageView(TemplateView, LoginRequiredMixin):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user
        starred_messages = StarredMessage.objects.filter(user=user).select_related('chat_message', 'assistant',
                                                                                   'organization', 'chat')

        org_assistants_messages = {}
        for message in starred_messages:
            org_name = message.organization.name
            assistant_name = message.assistant.name
            if org_name not in org_assistants_messages:
                org_assistants_messages[org_name] = {}
            if assistant_name not in org_assistants_messages[org_name]:
                org_assistants_messages[org_name][assistant_name] = []
            org_assistants_messages[org_name][assistant_name].append(message)
        context.update({'org_assistants_messages': org_assistants_messages, 'base_url': MEDIA_URL})
        return context


class DeleteStarredMessageView(LoginRequiredMixin, DeleteView):
    model = StarredMessage
    success_url = 'starred_messages:list'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        context_user = request.user
        starred_message = get_object_or_404(StarredMessage, id=self.kwargs['pk'])
        # PERMISSION CHECK FOR - STARRED_MESSAGES/REMOVE
        user_permissions = UserPermission.active_permissions.filter(user=context_user).all().values_list(
            'permission_type', flat=True
        )
        if PermissionNames.REMOVE_STARRED_MESSAGES not in user_permissions:
            messages.error(request, "You do not have permission to delete starred messages.")
            return redirect('starred_messages:list')
        starred_message.delete()
        print('[DeleteStarredMessageView.post] Starred message deleted successfully.')
        success_message = "Starred message deleted successfully."
        # assign the relevant message's starred field to False
        starred_message.chat_message.starred = False
        starred_message.chat_message.save()
        messages.success(request, success_message)
        return redirect(self.success_url)


