from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.starred_messages.models import StarredMessage
from apps.user_permissions.utils import PermissionNames
from config.settings import MEDIA_URL
from web_project import TemplateLayout


class ListStarredMessageView(TemplateView, LoginRequiredMixin):
    """
    Displays a list of starred messages for the authenticated user.

    This view retrieves and organizes starred messages by organization and assistant, allowing the user to easily browse through their saved messages.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with the list of starred messages grouped by organization and assistant.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_STARRED_MESSAGES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_STARRED_MESSAGES):
            messages.error(self.request, "You do not have permission to view starred messages.")
            return context
        ##############################

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
