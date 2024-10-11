#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: use_harmoniq_agent_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:34
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
import base64

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from apps.core.harmoniq.harmoniq_executor import OpenAIRealtimeAPIClient, sync_request_communication
from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.harmoniq.models import Harmoniq
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class HarmoniqView_Use(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - CHAT_WITH_HARMONIQ_AGENTS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.CHAT_WITH_HARMONIQ_AGENTS):
            messages.error(self.request, "You do not have permission to chat with Harmoniq Agents.")
            return context
        ##############################

        agents = Harmoniq.objects.filter(organization__users=self.request.user)
        context['agents'] = agents
        context['audio'] = None
        context['transcript'] = None
        return context


class HarmoniqCommunicationView(View):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        try:
            data = request.POST
            agent_id = data.get('agentPicker')
            msg = data.get('messageInput')
            if not agent_id or not msg:
                return JsonResponse({'error': 'Agent ID or message is missing'}, status=400)
            harmoniq_agent = Harmoniq.objects.get(id=agent_id)
            api_client = OpenAIRealtimeAPIClient(harmoniq_agent=harmoniq_agent, llm_model=harmoniq_agent.llm_model)
            sync_request_communication(api_client, msg)
            audio_data = base64.b64encode(api_client.audio_buffer).decode('utf-8')
            transcript_data = api_client.transcript
            return JsonResponse({'transcript': transcript_data, 'audio': audio_data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
