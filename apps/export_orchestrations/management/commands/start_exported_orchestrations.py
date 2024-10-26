#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#
#
#
#

import importlib

from django.core.management.base import BaseCommand
from django.urls import path

from apps.export_orchestrations.models import ExportOrchestrationAPI
from config import settings
from config.settings import EXPORT_ORCHESTRATION_API_BASE_URL, EXPORT_ORCHESTRATION_API_HEALTH_BASE_URL


def start_endpoint_for_orchestration(assistant: ExportOrchestrationAPI):
    from apps.export_orchestrations.views import ExportOrchestrationAPIView, ExportOrchestrationAPIHealthCheckView
    endpoint_url = assistant.endpoint
    endpoint_local = EXPORT_ORCHESTRATION_API_BASE_URL + endpoint_url.split(EXPORT_ORCHESTRATION_API_BASE_URL)[1]
    health_local = EXPORT_ORCHESTRATION_API_HEALTH_BASE_URL + endpoint_url.split(EXPORT_ORCHESTRATION_API_BASE_URL)[1]
    urlpatterns = getattr(importlib.import_module(settings.ROOT_URLCONF), 'urlpatterns')
    urlpatterns += [
        path(endpoint_local, ExportOrchestrationAPIView.as_view(), name=f'export_orchestration_{assistant.id}'),
        path(health_local, ExportOrchestrationAPIHealthCheckView.as_view(), name=f'export_orchestration_health_{assistant.id}'),
    ]


def initialize_orchestration_endpoints():
    for agent in ExportOrchestrationAPI.objects.all():
        agent: ExportOrchestrationAPI
        if agent.is_online:
            start_endpoint_for_orchestration(agent)
        else:
            # SKIP: OFFLINE
            pass


class Command(BaseCommand):
    help = 'Start all exported Orchestrators'

    def handle(self, *args, **kwargs):
        initialize_orchestration_endpoints()
