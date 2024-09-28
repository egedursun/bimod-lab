import importlib

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views import View

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.export_leanmods.management.commands.start_exported_leanmods import start_endpoint_for_leanmod
from apps.export_leanmods.models import ExportLeanmodAssistantAPI
from apps.user_permissions.utils import PermissionNames
from config import settings
from config.settings import EXPORT_LEANMOD_API_BASE_URL


class ToggleExportLeanmodAssistantServiceView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_EXPORT_LEANMOD
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_EXPORT_LEANMOD):
            messages.error(self.request, "You do not have permission to update Export LeanMod Assistant APIs.")
            return redirect('export_leanmods:list')
        ##############################

        export_assistant = get_object_or_404(ExportLeanmodAssistantAPI, pk=self.kwargs['pk'])
        endpoint = EXPORT_LEANMOD_API_BASE_URL + export_assistant.endpoint.split(EXPORT_LEANMOD_API_BASE_URL)[1]
        api_urls = getattr(importlib.import_module(settings.ROOT_URLCONF), 'urlpatterns')
        export_assistant.is_online = not export_assistant.is_online
        export_assistant.save()

        # Pause or start the endpoint based on the assistant's new online status
        if export_assistant.is_online:
            # check if the endpoint is already in the url patterns
            if not any(endpoint in str(url) for url in api_urls):
                start_endpoint_for_leanmod(export_assistant)
        return redirect('export_leanmods:list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
