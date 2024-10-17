#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: start_exported_leanmods.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:41
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

from apps.export_leanmods.models import ExportLeanmodAssistantAPI
from config import settings
from config.settings import EXPORT_LEANMOD_API_BASE_URL


def start_endpoint_for_leanmod(assistant: ExportLeanmodAssistantAPI):
    from apps.export_leanmods.views import ExportLeanmodAssistantAPIView
    endpoint_url = assistant.endpoint
    endpoint_local = EXPORT_LEANMOD_API_BASE_URL + endpoint_url.split(EXPORT_LEANMOD_API_BASE_URL)[1]
    urlpatterns = getattr(importlib.import_module(settings.ROOT_URLCONF), 'urlpatterns')
    urlpatterns += [
        path(endpoint_local, ExportLeanmodAssistantAPIView.as_view(), name=f'export_assistant_{assistant.id}')
    ]


def initialize_leanmod_endpoints():
    for assistant in ExportLeanmodAssistantAPI.objects.all():
        assistant: ExportLeanmodAssistantAPI
        if assistant.is_online:
            start_endpoint_for_leanmod(assistant)
        else:
            # OFFLINE: SKIP
            pass


class Command(BaseCommand):
    help = 'Start all exported LeanMod assistants'

    def handle(self, *args, **kwargs):
        initialize_leanmod_endpoints()
