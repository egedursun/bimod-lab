from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import DeleteView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DeleteAssistantView(LoginRequiredMixin, DeleteView):
    """
    Handles the deletion of an assistant.

    This view allows users with the appropriate permissions to delete an assistant. It checks if the user has the necessary permissions before performing the deletion.

    Methods:
        get_context_data(self, **kwargs): Adds the assistant to be deleted to the context for confirmation.
        post(self, request, *args, **kwargs): Deletes the assistant if the user has the required permissions.
        get_queryset(self): Filters the queryset to include only the assistants that belong to the user's organizations.
    """

    model = Assistant

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        assistant = self.get_object()
        context['assistant'] = assistant
        return context

    def post(self, request, *args, **kwargs):
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - DELETE_ASSISTANTS
        if not UserPermissionManager.is_authorized(user=context_user, operation=PermissionNames.DELETE_ASSISTANTS):
            messages.error(self.request, "You do not have permission to delete assistants.")
            return redirect('assistants:list')
        ##############################

        assistant = self.get_object()
        assistant.delete()
        return redirect('assistants:list')

    def get_queryset(self):
        context_user = self.request.user
        return Assistant.objects.filter(organization__users__in=[context_user])
