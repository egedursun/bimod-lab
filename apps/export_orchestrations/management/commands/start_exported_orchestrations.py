#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: start_exported_orchestrations.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:46
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

import importlib

from django.core.management.base import BaseCommand
from django.urls import path

from apps.export_orchestrations.models import ExportOrchestrationAPI
from config import settings
from config.settings import EXPORT_ORCHESTRATION_API_BASE_URL


def start_endpoint_for_orchestration(assistant: ExportOrchestrationAPI):
    from apps.export_orchestrations.views import ExportOrchestrationAPIView
    endpoint_url = assistant.endpoint
    endpoint_local = EXPORT_ORCHESTRATION_API_BASE_URL + endpoint_url.split(EXPORT_ORCHESTRATION_API_BASE_URL)[1]

    # Register the endpoint with Django's URL routing system
    urlpatterns = getattr(importlib.import_module(settings.ROOT_URLCONF), 'urlpatterns')
    urlpatterns += [
        path(endpoint_local, ExportOrchestrationAPIView.as_view(), name=f'export_assistant_{assistant.id}')
    ]
    print(f"[start_exported_orchestrations.start_endpoint_for_orchestration] Started endpoint for orchestrator {assistant.orchestrator.name} at {endpoint_local}")


def initialize_orchestration_endpoints():
    for assistant in ExportOrchestrationAPI.objects.all():
        assistant: ExportOrchestrationAPI
        if assistant.is_online:
            start_endpoint_for_orchestration(assistant)
        else:
            print(f"[start_exported_orchestrations.initialize_orchestration_endpoints] Export orchestrator {assistant.orchestrator.name} is offline. Skipping...")


class Command(BaseCommand):
    help = 'Start all exported Orchestrators'

    def handle(self, *args, **kwargs):
        initialize_orchestration_endpoints()
