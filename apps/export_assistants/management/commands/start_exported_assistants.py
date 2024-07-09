import importlib

from django.core.management.base import BaseCommand
from django.urls import path

from apps.export_assistants.models import ExportAssistantAPI
from config import settings
from config.settings import EXPORT_API_BASE_URL


def start_endpoint_for_assistant(assistant):
    from apps.export_assistants.views import ExportAssistantAPIView
    endpoint_url = assistant.endpoint
    endpoint_local = EXPORT_API_BASE_URL + endpoint_url.split(EXPORT_API_BASE_URL)[1]

    # Register the endpoint with Django's URL routing system
    urlpatterns = getattr(importlib.import_module(settings.ROOT_URLCONF), 'urlpatterns')
    urlpatterns += [
        path(endpoint_local, ExportAssistantAPIView.as_view(), name=f'export_assistant_{assistant.id}')
    ]
    print(f"Started endpoint for assistant {assistant.assistant.name} at {endpoint_local}")


def initialize_endpoints():
    for assistant in ExportAssistantAPI.objects.all():
        if assistant.is_online:
            start_endpoint_for_assistant(assistant)
        else:
            print(f"Export assistant {assistant.assistant.name} is offline. Skipping...")


class Command(BaseCommand):
    help = 'Start all exported assistants'

    def handle(self, *args, **kwargs):
        initialize_endpoints()
