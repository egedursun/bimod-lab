from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DeleteView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.message_templates.models import MessageTemplate
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DeleteMessageTemplateView(DeleteView, LoginRequiredMixin):
    """
    Handles the deletion of a message template.

    This view allows users to delete a specific message template, provided they have the necessary permissions.

    Methods:
        get_context_data(self, **kwargs): Prepares the context for the deletion confirmation page.
        post(self, request, *args, **kwargs): Processes the deletion of the specified message template.
    """

    model = MessageTemplate
    success_url = 'message_templates:list'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - REMOVE_TEMPLATE_MESSAGES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.REMOVE_TEMPLATE_MESSAGES):
            messages.error(self.request, "You do not have permission to delete template messages.")
            return redirect('message_templates:list')
        ##############################

        starred_message = get_object_or_404(MessageTemplate, id=self.kwargs['pk'])
        starred_message.delete()
        success_message = "Message template deleted successfully."
        print('[DeleteMessageTemplateView.post] Message template deleted successfully.')
        messages.success(request, success_message)
        return redirect(self.success_url)
