from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.message_templates.models import MessageTemplate
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class ListMessageTemplateView(TemplateView, LoginRequiredMixin):
    """
    Displays a list of message templates created by the user.

    This view retrieves and displays all message templates that the current user has created.

    Methods:
        get_context_data(self, **kwargs): Retrieves the user's message templates and adds them to the context.
    """

    model = MessageTemplate

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_TEMPLATE_MESSAGES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_TEMPLATE_MESSAGES):
            messages.error(self.request, "You do not have permission to list template messages.")
            return context
        ##############################

        context['message_templates'] = MessageTemplate.objects.filter(user=self.request.user)
        return context
