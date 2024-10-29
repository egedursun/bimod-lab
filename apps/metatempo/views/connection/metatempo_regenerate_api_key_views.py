#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: metakanban_regenerate_api_key_views.py
#  Last Modified: 2024-10-28 20:32:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-28 20:32:11
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
import json
import secrets

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View

from apps.metatempo.models import MetaTempoConnection
from apps.metatempo.utils import META_TEMPO_CONNECTION_API_KEY_DEFAULT_LENGTH


class MetaTempoView_ConnectionRegenerateAPIKey(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            connection_id_text = data.get('connection_id')
            connection_id = int(connection_id_text)
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            messages.error(request, "Invalid connection ID.")
            return JsonResponse({'error': 'Invalid connection ID.'}, status=400)

        try:
            connection = MetaTempoConnection.objects.get(id=connection_id)
            new_api_key = secrets.token_urlsafe(META_TEMPO_CONNECTION_API_KEY_DEFAULT_LENGTH)
            connection.connection_api_key = new_api_key
            connection.save()
        except MetaTempoConnection.DoesNotExist:
            messages.error(request, "Connection not found.")
            return JsonResponse({'error': 'Connection not found.'}, status=404)
        except Exception as e:
            messages.error(request, "Failed to regenerate API key.")
            return JsonResponse({'error': 'Failed to regenerate API key.'}, status=500)

        messages.success(request, "API key regenerated successfully.")
        return JsonResponse({'new_token': new_api_key}, status=200)
