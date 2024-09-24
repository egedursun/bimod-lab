import importlib

from django.core.management.base import BaseCommand
from django.urls import path

from apps.export_assistants.models import ExportAssistantAPI
from apps.export_leanmods.models import ExportLeanmodAssistantAPI
from config import settings
from config.settings import EXPORT_API_BASE_URL, EXPORT_LEANMOD_API_BASE_URL


def start_endpoint_for_leanmod(assistant: ExportLeanmodAssistantAPI):
    from apps.export_leanmods.views import ExportLeanmodAssistantAPIView
    endpoint_url = assistant.endpoint
    endpoint_local = EXPORT_LEANMOD_API_BASE_URL + endpoint_url.split(EXPORT_LEANMOD_API_BASE_URL)[1]

    # Register the endpoint with Django's URL routing system
    urlpatterns = getattr(importlib.import_module(settings.ROOT_URLCONF), 'urlpatterns')
    urlpatterns += [
        path(endpoint_local, ExportLeanmodAssistantAPIView.as_view(), name=f'export_assistant_{assistant.id}')
    ]
    print(f"[start_exported_leanmods.start_endpoint_for_leanmod] Started endpoint for assistant {assistant.lean_assistant.name} at {endpoint_local}")


def initialize_leanmod_endpoints():
    for assistant in ExportLeanmodAssistantAPI.objects.all():
        assistant: ExportLeanmodAssistantAPI
        if assistant.is_online:
            start_endpoint_for_leanmod(assistant)
        else:
            print(f"[start_exported_leanmods.initialize_leanmod_endpoints] Export assistant {assistant.lean_assistant.name} is offline. Skipping...")


class Command(BaseCommand):
    help = 'Start all exported LeanMod assistants'

    def handle(self, *args, **kwargs):
        initialize_leanmod_endpoints()
