import importlib

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.export_assistants.models import ExportAssistantAPI
from apps.user_permissions.models import PermissionNames
from config import settings
from config.settings import EXPORT_API_BASE_URL


class ToggleExportAssistantServiceView(LoginRequiredMixin, View):
    """
    Toggles the online/offline status of an Export Assistant API.

    This view allows users with the appropriate permissions to toggle an Export Assistant API's availability by either starting or pausing its endpoint.

    Methods:
        post(self, request, *args, **kwargs): Toggles the assistant's online status and starts or stops the endpoint accordingly.
    """

    def post(self, request, *args, **kwargs):
        from apps.export_assistants.management.commands.start_exported_assistants import start_endpoint_for_assistant

        export_assistant = get_object_or_404(ExportAssistantAPI, pk=self.kwargs['pk'])
        endpoint = EXPORT_API_BASE_URL + export_assistant.endpoint.split(EXPORT_API_BASE_URL)[1]
        context_user = request.user

        ##############################
        # PERMISSION CHECK FOR - UPDATE_EXPORT_ASSISTANT
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_EXPORT_ASSIST):
            messages.error(self.request, "You do not have permission to update Export Assistant APIs.")
            return redirect('export_assistants:list')
        ##############################

        api_urls = getattr(importlib.import_module(settings.ROOT_URLCONF), 'urlpatterns')
        export_assistant.is_online = not export_assistant.is_online
        export_assistant.save()

        # Pause or start the endpoint based on the assistant's new online status
        if export_assistant.is_online:
            # check if the endpoint is already in the url patterns
            if not any(endpoint in str(url) for url in api_urls):
                start_endpoint_for_assistant(export_assistant)
        return redirect('export_assistants:list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
