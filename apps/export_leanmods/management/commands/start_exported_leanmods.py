#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: start_exported_leanmods.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:39
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: start_exported_leanmods.py
#  Last Modified: 2024-09-25 17:51:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:51:13
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

from apps.export_leanmods.models import ExportLeanmodAssistantAPI
from config import settings
from config.settings import EXPORT_LEANMOD_API_BASE_URL


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
