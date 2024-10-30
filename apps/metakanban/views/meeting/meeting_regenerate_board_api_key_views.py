#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: meeting_regenerate_board_api_key_views.py
#  Last Modified: 2024-10-28 17:00:19
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-28 17:00:19
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

from apps.metakanban.models import MetaKanbanBoard
from apps.metakanban.utils import META_KANBAN_BOARD_API_KEY_DEFAULT_LENGTH


class MetaKanbanView_MeetingRegenerateAPIKey(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        try:
            board_id_text = data.get('board_id')
            board_id = int(board_id_text)
        except Exception as e:
            messages.error(request, "Invalid board ID.")
            return JsonResponse({'error': 'Invalid board ID.'})
        try:
            board = MetaKanbanBoard.objects.get(id=board_id)
            new_api_key = secrets.token_urlsafe(META_KANBAN_BOARD_API_KEY_DEFAULT_LENGTH)
            board.connection_api_key = new_api_key
            board.save()
        except Exception as e:
            messages.error(request, "Failed to regenerate API key.")
            return JsonResponse({'error': 'Failed to regenerate API key.'})

        messages.success(request, "API key regenerated successfully.")
        return JsonResponse({'new_token': new_api_key})
