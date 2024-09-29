#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: start_exported_assistants.py
#  Last Modified: 2024-09-27 19:45:58
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:50:10
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

import importlib

from django.core.management.base import BaseCommand
from django.urls import path

from apps.export_assistants.models import ExportAssistantAPI
from apps.export_assistants.views.endpoints import ExportAssistantAPIView
from config import settings
from config.settings import EXPORT_API_BASE_URL


def start_endpoint_for_assistant(assistant):
    endpoint_url = assistant.endpoint
    endpoint_local = EXPORT_API_BASE_URL + endpoint_url.split(EXPORT_API_BASE_URL)[1]

    # Register the endpoint with Django's URL routing system
    urlpatterns = getattr(importlib.import_module(settings.ROOT_URLCONF), 'urlpatterns')
    urlpatterns += [
        path(endpoint_local, ExportAssistantAPIView.as_view(), name=f'export_assistant_{assistant.id}')
    ]
    print(f"[start_exported_assistants.initialize_endpoints] Started endpoint for assistant {assistant.assistant.name} at {endpoint_local}")


def initialize_endpoints():
    for assistant in ExportAssistantAPI.objects.all():
        if assistant.is_online:
            start_endpoint_for_assistant(assistant)
        else:
            print(f"[start_exported_assistants.initialize_endpoints] Export assistant {assistant.assistant.name} is offline. Skipping...")


class Command(BaseCommand):
    help = 'Start all exported assistants'

    def handle(self, *args, **kwargs):
        initialize_endpoints()
