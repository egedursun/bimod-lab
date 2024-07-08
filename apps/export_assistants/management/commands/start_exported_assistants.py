import importlib

from django.core.management.base import BaseCommand
from django.urls import path

from apps.export_assistants.models import ExportAssistantAPI
from config import settings
from config.settings import EXPORT_API_VERSION


def start_endpoint_for_assistant(assistant):
    from apps.export_assistants.views import ExportAssistantAPIView
    endpoint_url = f'api/{EXPORT_API_VERSION}/exported/{assistant.endpoint}'

    # Register the endpoint with Django's URL routing system
    urlpatterns = getattr(importlib.import_module(settings.ROOT_URLCONF), 'urlpatterns')
    urlpatterns += [
        path(endpoint_url, ExportAssistantAPIView.as_view(), name=f'export_assistant_{assistant.id}')
    ]
    print(f"Started endpoint for assistant {assistant.assistant.name} at {endpoint_url}")


def initialize_endpoints():
    for assistant in ExportAssistantAPI.objects.all():
        start_endpoint_for_assistant(assistant)


class Command(BaseCommand):
    help = 'Start all exported assistants'

    def handle(self, *args, **kwargs):
        initialize_endpoints()
