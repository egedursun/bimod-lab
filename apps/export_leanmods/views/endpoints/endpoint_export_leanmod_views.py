#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: endpoint_export_leanmod_views.py
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

import json
import logging
import re

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.core.generative_ai.generative_ai_decode_manager import GenerativeAIDecodeController
from apps.export_leanmods.models import ExportLeanmodAssistantAPI, LeanmodRequestLog
from apps.export_leanmods.utils import LeanModAssistantStatusCodes
from apps.multimodal_chat.models import MultimodalLeanChat, MultimodalLeanChatMessage
from apps.multimodal_chat.utils import generate_chat_name, SourcesForMultimodalChatsNames
from config.consumers import APIExportTypesNames
from config.settings import BASE_URL

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class ExportLeanmodAssistantAPIHealthCheckView(View):
    def post(self, request, *args, **kwargs):

        endpoint = request.path
        pattern = r'^/app/export_leanmods/health/leanmod_assistants/(?P<organization_id>\d+)/(?P<assistant_id>\d+)/(?P<export_id>\d+)/$'
        match = re.match(pattern, endpoint)

        if match:
            organization_id = int(match.group('organization_id'))
            assistant_id = int(match.group('assistant_id'))
            export_id = int(match.group('export_id'))

        else:

            return JsonResponse(
                {
                    "message": "Invalid path parameters.",
                    "data": {},
                    "status": LeanModAssistantStatusCodes.NOT_FOUND
                },
                status=LeanModAssistantStatusCodes.NOT_FOUND
            )

        try:
            export_assistant = ExportLeanmodAssistantAPI.objects.get(id=export_id)

        except ExportLeanmodAssistantAPI.DoesNotExist:

            logger.error(f"Invalid LeanMod endpoint: {endpoint}")

            return JsonResponse(
                {
                    "message": "Invalid LeanMod endpoint",
                    "data": {},
                    "status": LeanModAssistantStatusCodes.NOT_FOUND
                },
                status=LeanModAssistantStatusCodes.NOT_FOUND
            )

        if not export_assistant.is_online:
            logger.error(f"The LeanMod  is currently offline: {endpoint}")
            return JsonResponse(
                {
                    "message": "The LeanMod endpoint is currently offline. Please try again later.",
                    "data": {},
                    "status": LeanModAssistantStatusCodes.SERVICE_OFFLINE
                },
                status=LeanModAssistantStatusCodes.SERVICE_OFFLINE
            )

        return JsonResponse(
            {
                "message": "The LeanMod endpoint is online and healthy.",
                "data": {},
                "status": LeanModAssistantStatusCodes.OK
            },
            status=LeanModAssistantStatusCodes.OK
        )


@method_decorator(csrf_exempt, name='dispatch')
class ExportLeanmodAssistantAPIView(View):
    def post(self, request, *args, **kwargs):
        endpoint = request.path
        pattern = r'^/app/export_leanmods/exported/leanmod_assistants/(?P<organization_id>\d+)/(?P<assistant_id>\d+)/(?P<export_id>\d+)/$'
        match = re.match(pattern, endpoint)

        if match:
            organization_id = int(match.group('organization_id'))
            assistant_id = int(match.group('assistant_id'))
            export_id = int(match.group('export_id'))

        else:

            return JsonResponse(
                {
                    "message": "Invalid path parameters.",
                    "data": {},
                    "status": LeanModAssistantStatusCodes.NOT_FOUND
                },
                status=LeanModAssistantStatusCodes.NOT_FOUND
            )

        api_key = request.headers.get('Authorization')

        try:
            exp_agent = ExportLeanmodAssistantAPI.objects.get(
                id=export_id
            )

        except ExportLeanmodAssistantAPI.DoesNotExist:

            logger.error(f"Invalid LeanMod endpoint: {endpoint}")
            return JsonResponse(
                {
                    "message": "Invalid LeanMod endpoint",
                    "data": {},
                    "status": LeanModAssistantStatusCodes.NOT_FOUND
                },
                status=LeanModAssistantStatusCodes.NOT_FOUND
            )

        if not exp_agent.is_online:
            logger.error(f"The LeanMod endpoint is currently offline: {endpoint}")
            return JsonResponse(
                {
                    "message": "The LeanMod endpoint is currently offline. Please try again later.",
                    "data": {},
                    "status": LeanModAssistantStatusCodes.SERVICE_OFFLINE
                },
                status=LeanModAssistantStatusCodes.SERVICE_OFFLINE
            )

        if (not exp_agent.is_public) and exp_agent.custom_api_key != api_key:
            logger.error(f"Invalid LeanMod API key provided for endpoint: {endpoint}")

            return JsonResponse(
                {
                    "message": "The LeanMod API key provided is invalid, please provide a valid API key.",
                    "data": {},
                    "status": LeanModAssistantStatusCodes.UNAUTHORIZED
                },
                status=LeanModAssistantStatusCodes.UNAUTHORIZED
            )

        LeanmodRequestLog.objects.create(export_lean_assistant=exp_agent)
        if exp_agent.requests_in_last_hour() > exp_agent.request_limit_per_hour:
            logger.error(f"The API request limit has been reached for endpoint: {endpoint}")
            return JsonResponse(
                {
                    "error": "The API request limit has been reached. Please try again later.",
                    "data": {
                        "request_limit_per_hour": exp_agent.request_limit_per_hour,
                        "requests_in_last_hour": exp_agent.requests_in_last_hour()
                    },
                },
                status=LeanModAssistantStatusCodes.TOO_MANY_REQUESTS
            )

        body = json.loads(request.body)

        try:
            chat_history = body.get('chat_history', [])

            options = body.get('options', {})

            process_log_streaming_enabled = False
            if "streaming_options" in options:
                streaming_options = options.get("streaming_options", {})

                if "process_log_streaming" in streaming_options:
                    process_log_streaming_enabled = streaming_options.get("process_log_streaming", False)
                else:
                    pass
            else:
                pass

            if len(chat_history) == 0:
                logger.error("Chat history is empty.")
                raise ValueError("Chat history is empty.")

            api_chat = MultimodalLeanChat.objects.create(
                organization=exp_agent.lean_assistant.organization,
                lean_assistant=exp_agent.lean_assistant,
                user=exp_agent.created_by_user,
                chat_name=generate_chat_name(),
                created_by_user=exp_agent.created_by_user,
                chat_source=SourcesForMultimodalChatsNames.API
            )

            user_message = None
            for message in chat_history:
                role = message["role"]
                content = message["content"]
                file_uris = []
                image_uris = []

                if "file_uris" in message and message["file_uris"] != "":
                    file_uris = message.get("file_uris", "").split(",") if message.get("file_uris") else []

                if "image_uris" in message and message["image_uris"] != "":
                    image_uris = message.get("image_uris", "").split(",") if message.get("image_uris") else []

                file_uris = [uri.strip() for uri in file_uris if uri.strip()] if file_uris else []
                image_uris = [uri.strip() for uri in image_uris if uri.strip()]

                api_chat.lean_chat_messages.create(
                    multimodal_lean_chat=api_chat,
                    sender_type=role.upper(),
                    message_text_content=content,
                    message_file_contents=file_uris,
                    message_image_contents=image_uris
                )

                user_message = api_chat.lean_chat_messages.filter(
                    sender_type=role.upper()
                ).last()

        except Exception as e:
            logger.error(f"Invalid chat history provided: {str(e)}")

            return JsonResponse(
                {
                    "message": "Internal server error: " + str(e),
                    "data": {},
                    "status": LeanModAssistantStatusCodes.INTERNAL_SERVER_ERROR
                },
                status=LeanModAssistantStatusCodes.INTERNAL_SERVER_ERROR
            )

        try:
            llm_client = GenerativeAIDecodeController.get_lean(
                assistant=exp_agent.lean_assistant,
                multimodal_chat=api_chat,
                user=exp_agent.created_by_user
            )

            llm_response_text, file_uris, image_uris = llm_client.respond_stream(
                latest_message=user_message,
                with_media=True,
                fermion__is_fermion_supervised=process_log_streaming_enabled,
                fermion__export_type=APIExportTypesNames.LEANMOD,
                fermion__endpoint=endpoint
            )

            MultimodalLeanChatMessage.objects.create(
                multimodal_lean_chat=api_chat,
                sender_type='ASSISTANT',
                message_text_content=llm_response_text
            )

        except Exception as e:
            logger.error(f"Error generating response for endpoint: {endpoint}")
            return JsonResponse(
                {
                    "message": "Internal server error: " + str(e),
                    "data": {},
                    "status": LeanModAssistantStatusCodes.INTERNAL_SERVER_ERROR
                },
                status=LeanModAssistantStatusCodes.INTERNAL_SERVER_ERROR
            )

        response_data = {
            "message": "Success",
            "data": {
                "metadata": {
                    "organization": {
                        "organization_name": exp_agent.lean_assistant.organization.name
                    },
                    "assistant": {
                        "assistant_name": exp_agent.lean_assistant.name
                    },
                    "chat": {
                        "chat_name": api_chat.chat_name
                    }
                },
                "message": {
                    "assistant_name": exp_agent.lean_assistant.name,
                    "content": llm_response_text,
                    "role": "assistant",
                    "media": {
                        "files": file_uris,
                        "images": image_uris
                    }
                }
            }
        }

        logger.info(f"Leanmod Assistant API response generated for endpoint: {endpoint}")
        return JsonResponse(
            response_data,
            status=LeanModAssistantStatusCodes.OK
        )
