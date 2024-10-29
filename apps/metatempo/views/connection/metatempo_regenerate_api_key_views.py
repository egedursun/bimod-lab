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
from django.shortcuts import redirect
from django.views import View

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.metatempo.models import MetaTempoConnection
from apps.metatempo.utils import META_TEMPO_CONNECTION_API_KEY_DEFAULT_LENGTH
from apps.user_permissions.utils import PermissionNames


class MetaTempoView_ConnectionRegenerateAPIKey(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_METATEMPO_CONNECTION
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_METATEMPO_CONNECTION):
            messages.error(self.request, "You do not have permission to update a MetaTempo Connection.")
            return JsonResponse({'error': 'You do not have permission to update a MetaTempo Connection.'}, status=403)
        ##############################

        connection_id = kwargs.get('connection_id')
        if not connection_id:
            messages.error(request, "Connection ID not provided.")
            return JsonResponse({'error': 'Connection ID not provided.'}, status=400)
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
