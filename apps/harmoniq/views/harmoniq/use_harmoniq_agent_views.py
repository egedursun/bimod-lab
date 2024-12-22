#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#

import base64
import logging

from django.contrib import messages

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.http import JsonResponse
from django.views import View

from django.views.decorators.csrf import (
    csrf_exempt
)

from django.views.generic import TemplateView

from apps.core.generative_ai.utils import (
    find_tool_call_from_json
)

from apps.core.harmoniq.harmoniq_executor import (
    OpenAIRealtimeAPIClient,
    sync_request_communication
)

from apps.core.harmoniq.harmoniq_tool_manager import (
    HarmoniqToolManager
)

from apps.core.harmoniq.utils import (
    MAX_ATTEMPTS_TOOL_CALL
)

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.harmoniq.models import Harmoniq

from apps.leanmod.models import (
    ExpertNetwork,
    ExpertNetworkAssistantReference
)

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class HarmoniqView_Use(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - CHAT_WITH_HARMONIQ_AGENTS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.CHAT_WITH_HARMONIQ_AGENTS
        ):
            messages.error(self.request, "You do not have permission to chat with Harmoniq Agents.")
            return context
        ##############################

        agents = Harmoniq.objects.filter(
            organization__users=self.request.user
        )

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
                return JsonResponse(
                    {
                        'error': 'Agent ID or message is missing'
                    },
                    status=400
                )

            harmoniq_agent = Harmoniq.objects.get(
                id=agent_id
            )

            org = harmoniq_agent.organization
            user = self.request.user

            org_data = {
                "org_id": org.id,
                "org_name": org.name,
                "org_address": org.address,
                "org_phone": org.phone,
                "org_city": org.city,
                "org_country": org.country,
                "org_postal_code": org.postal_code,
                "org_industry": org.industry,
            }

            user_data = {
                "username": user.username,
                "email": user.email,
                "first_name": user.profile.first_name,
                "last_name": user.profile.last_name,
                "phone": user.profile.phone_number,
                "address": user.profile.address,
                "city": user.profile.city,
                "country": user.profile.country,
                "postal_code": user.profile.postal_code
            }

            expert_net_and_refs = {}

            for expert_net in harmoniq_agent.consultant_expert_networks.all():
                expert_net: ExpertNetwork

                expert_net_and_refs[expert_net.name] = {
                    "expert_network_name": expert_net.name,
                    "meta_description": expert_net.meta_description,
                    "assistant_references": {}
                }

                for ref in expert_net.assistant_references.all():
                    ref: ExpertNetworkAssistantReference

                    expert_net_and_refs[expert_net.name]["assistant_references"][ref.id] = {
                        "assistant_id": ref.id,
                        "assistant_name": ref.assistant.name,
                        "context_instructions": ref.context_instructions
                    }

            api_client = OpenAIRealtimeAPIClient(
                harmoniq_agent=harmoniq_agent,
                llm_model=harmoniq_agent.llm_model,
                expert_net_and_refs=expert_net_and_refs,
                org_data=org_data,
                user_data=user_data
            )

            sync_request_communication(api_client, msg)

            audio_data = base64.b64encode(api_client.audio_buffer).decode('utf-8')
            transcript_data = api_client.transcript

            def process_tool_calls(
                transcript,
                audio,
                attempt=0
            ):

                if attempt > MAX_ATTEMPTS_TOOL_CALL:
                    logger.error(f"Tool calls are not successful after {MAX_ATTEMPTS_TOOL_CALL} attempts.")

                    return transcript, audio

                json_content_of_resp = find_tool_call_from_json(transcript)

                if not json_content_of_resp:
                    logger.info("No tool call found in the transcript.")

                    return transcript, audio

                tool_resp_list = []
                for i, tool_call in enumerate(json_content_of_resp):
                    tool_xc = HarmoniqToolManager(
                        agent=harmoniq_agent,
                        tool_usage_json_str=tool_call
                    )

                    tool_resp, tool_name, file_uris, image_uris = tool_xc.call_internal_tool_service_harmoniq()

                    tool_resp_list.append(
                        f"""
                            [{i}] "tool_name": {tool_name},
                                [{i}a.] "tool_response": {tool_resp},
                                [{i}b.] "file_uris": {file_uris},
                                [{i}c.] "image_uris": {image_uris}
                        """
                    )

                tool_msg = f"""
                    ---
                    Tool Response List:

                    ### **VERY IMPORTANT NOTE:**

                    (Although you don't remember, you have requested for this output in your previous response, and
                    you wanted this to answer the user's questions. Thus, don't attempt to do another tool call, as
                    if you see data below, this means that the tool response is already achieved, and answer
                    accordingly.

                    ---

                    {str(tool_resp_list)}

                    ---
                """

                updated_msg = (msg + tool_msg)

                sync_request_communication(
                    api_client,
                    updated_msg
                )

                updated_audio_data = base64.b64encode(
                    api_client.audio_buffer
                ).decode('utf-8')

                updated_transcript_data = api_client.transcript

                logger.info(f"Tool calls are successful after {attempt + 1} attempts.")

                return process_tool_calls(
                    updated_transcript_data,
                    updated_audio_data,
                    attempt + 1
                )

            final_transcript, final_audio = process_tool_calls(transcript_data, audio_data)
            logger.info(f"Communication is successful.")

            return JsonResponse(
                {
                    'transcript': final_transcript,
                    'audio': final_audio
                }
            )

        except Exception as e:
            logger.error(f"Communication is not successful. Error: {str(e)}")

            return JsonResponse(
                {
                    'error': str(e)
                },
                status=400
            )
