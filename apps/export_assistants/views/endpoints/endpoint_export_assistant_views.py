#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: endpoint_export_assistant_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:44
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

from apps.assistants.models import Assistant
from apps.export_assistants.models import ExportAssistantAPI, RequestLog
from apps.export_assistants.utils import ExportAPIStatusCodes
from apps.multimodal_chat.models import MultimodalChat, MultimodalChatMessage
from apps.multimodal_chat.utils import generate_chat_name, SourcesForMultimodalChatsNames
from apps.organization.models import Organization
from config.consumers import APIExportTypesNames

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name="dispatch")
class ExportAssistantAPIHealthCheckView(View):
    def post(self, request, *args, **kwargs):
        endpoint = request.path
        pattern = r'^/app/export_assistants/health/assistants/(?P<organization_id>\d+)/(?P<assistant_id>\d+)/(?P<export_id>\d+)/$'
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
                    "status": ExportAPIStatusCodes.NOT_FOUND
                },
                status=ExportAPIStatusCodes.NOT_FOUND
            )

        try:
            export_assistant = ExportAssistantAPI.objects.get(id=export_id)

        except ExportAssistantAPI.DoesNotExist:

            logger.error(f"Invalid Assistant endpoint: {endpoint}")
            return JsonResponse(
                {
                    "message": "Invalid Assistant endpoint",
                    "data": {},
                    "status": ExportAPIStatusCodes.NOT_FOUND
                },
                status=ExportAPIStatusCodes.NOT_FOUND
            )

        if not export_assistant.is_online:
            logger.error(f"The Assistant endpoint is currently offline: {endpoint}")

            return JsonResponse(
                {
                    "message": "The Assistant endpoint is currently offline. Please try again later.",
                    "data": {},
                    "status": ExportAPIStatusCodes.SERVICE_OFFLINE
                },
                status=ExportAPIStatusCodes.SERVICE_OFFLINE
            )

        return JsonResponse(
            {
                "message": "The Assistant endpoint is online and healthy.",
                "data": {},
                "status": ExportAPIStatusCodes.OK
            },
            status=ExportAPIStatusCodes.OK
        )


@method_decorator(csrf_exempt, name='dispatch')
class ExportAssistantAPIView(View):
    def post(self, request, *args, **kwargs):
        endpoint = request.path
        pattern = r'^/app/export_assistants/exported/assistants/(?P<organization_id>\d+)/(?P<assistant_id>\d+)/(?P<export_id>\d+)/$'
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
                    "status": ExportAPIStatusCodes.NOT_FOUND
                },
                status=ExportAPIStatusCodes.NOT_FOUND
            )

        api_key = request.headers.get('Authorization')

        try:

            organization = Organization.objects.get(id=organization_id)
            if not organization:
                logger.error(f"Invalid organization ID provided for endpoint: {endpoint}")
                return JsonResponse(
                    {
                        "message": "Invalid organization ID provided",
                        "data": {},
                        "status": ExportAPIStatusCodes.NOT_FOUND
                    },
                    status=ExportAPIStatusCodes.NOT_FOUND
                )

            assistant = Assistant.objects.get(id=assistant_id)
            if not assistant:
                logger.error(f"Invalid assistant ID provided for endpoint: {endpoint}")
                return JsonResponse(
                    {
                        "message": "Invalid assistant ID provided",
                        "data": {},
                        "status": ExportAPIStatusCodes.NOT_FOUND
                    },
                    status=ExportAPIStatusCodes.NOT_FOUND
                )

            export_assistant = ExportAssistantAPI.objects.get(id=export_id)
            if not export_assistant:
                logger.error(f"Invalid export assistant ID provided for endpoint: {endpoint}")
                return JsonResponse(
                    {
                        "message": "Invalid export assistant ID provided", "data": {},
                        "status": ExportAPIStatusCodes.NOT_FOUND
                    },
                    status=ExportAPIStatusCodes.NOT_FOUND
                )

        except ExportAssistantAPI.DoesNotExist:

            logger.error(f"Invalid Assistant endpoint: {endpoint}")

            return JsonResponse(
                {
                    "message": "Invalid Assistant endpoint",
                    "data": {},
                    "status": ExportAPIStatusCodes.NOT_FOUND
                },
                status=ExportAPIStatusCodes.NOT_FOUND
            )

        if not export_assistant.is_online:
            logger.error(f"The Assistant endpoint is currently offline: {endpoint}")
            return JsonResponse(
                {
                    "message": "The Assistant endpoint is currently offline. Please try again later.",
                    "data": {},
                    "status": ExportAPIStatusCodes.SERVICE_OFFLINE
                },
                status=ExportAPIStatusCodes.SERVICE_OFFLINE
            )

        if (not export_assistant.is_public) and export_assistant.custom_api_key != api_key:
            logger.error(f"Invalid Assistant API key provided for endpoint: {endpoint}")
            return JsonResponse(
                {
                    "message": "The Assistant API key provided is invalid, please provide a valid API key.",
                    "data": {},
                    "status":
                        ExportAPIStatusCodes.UNAUTHORIZED
                }, status=ExportAPIStatusCodes.UNAUTHORIZED
            )

        RequestLog.objects.create(export_assistant=export_assistant)

        if export_assistant.requests_in_last_hour() > export_assistant.request_limit_per_hour:
            logger.error(f"The Assistant API request limit has been reached for endpoint: {endpoint}")
            return JsonResponse(
                {
                    "error": "The Assistant API request limit has been reached. Please try again later.",
                    "data": {
                        "request_limit_per_hour": export_assistant.request_limit_per_hour,
                        "requests_in_last_hour": export_assistant.requests_in_last_hour()
                    },
                },
                status=ExportAPIStatusCodes.TOO_MANY_REQUESTS
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
                logger.error(f"Invalid chat history provided for endpoint, no chat history error: {endpoint}")
                raise ValueError("Chat history is empty.")

            if "role" not in chat_history[0]:
                logger.error(f"Invalid chat history provided for endpoint, not existent role field error: {endpoint}")
                raise ValueError("Each of the chat history elements must contain 'role' key, which can either"
                                 "be 'system', 'assistant' or 'user'.")

            if chat_history[0]["role"] not in [
                "system",
                "assistant",
                "user"
            ]:
                logger.error(f"Invalid chat history provided for endpoint, invalid role error: {endpoint}")
                raise ValueError("The 'role' key in the first element of the chat history must be either 'system',"
                                 "'assistant' or 'user'.")

            if "content" not in chat_history[0]:
                logger.error(
                    f"Invalid chat history provided for endpoint, no content in chat history element: {endpoint}")
                raise ValueError("Each of the chat history elements must contain 'content' key.")

            if not isinstance(chat_history[0]["content"], str):
                logger.error(f"Invalid chat history provided for endpoint, content field error: {endpoint}")
                raise ValueError("The 'content' key in the first element of the chat history must be a string.")

        except Exception as e:
            logger.error(f"Invalid chat history provided for endpoint, {e}: {endpoint}")
            return JsonResponse(
                {
                    "message": "Internal server error: " + str(e),
                    "data": {},
                    "status": ExportAPIStatusCodes.INTERNAL_SERVER_ERROR
                },
                status=ExportAPIStatusCodes.INTERNAL_SERVER_ERROR
            )

        api_chat = MultimodalChat.objects.create(
            organization=export_assistant.assistant.organization,
            assistant=export_assistant.assistant,
            user=export_assistant.created_by_user,
            chat_name=generate_chat_name(),
            created_by_user=export_assistant.created_by_user,
            chat_source=SourcesForMultimodalChatsNames.API
        )

        user_msg = None
        try:

            for msg in chat_history:

                role = msg["role"]
                content = msg["content"]
                f_uris = []
                img_uris = []

                if "file_uris" in msg and msg["file_uris"] != "":
                    f_uris = msg.get("file_uris", "").split(",") if msg.get("file_uris") else []

                if "image_uris" in msg and msg["image_uris"] != "":
                    img_uris = msg.get("image_uris", "").split(",") if msg.get("image_uris") else []

                f_uris = [uri.strip() for uri in f_uris if uri.strip()] if f_uris else []
                img_uris = [uri.strip() for uri in img_uris if uri.strip()]

                api_chat.chat_messages.create(
                    multimodal_chat=api_chat,
                    sender_type=role.upper(),
                    message_text_content=content,
                    message_file_contents=f_uris,
                    message_image_contents=img_uris
                )

                user_msg = api_chat.chat_messages.filter(sender_type=role.upper()).last()

        except Exception as e:
            logger.error(f"Invalid chat history provided for endpoint, {e}: {endpoint}")
            return JsonResponse({
                "message": "Internal server error: " + str(e),
                "data": {}, "status": ExportAPIStatusCodes.INTERNAL_SERVER_ERROR
            }, status=ExportAPIStatusCodes.INTERNAL_SERVER_ERROR)

        try:
            from apps.core.generative_ai.generative_ai_decode_manager import GenerativeAIDecodeController

            llm_client = GenerativeAIDecodeController.get(
                assistant=export_assistant.assistant,
                multimodal_chat=api_chat
            )

            llm_response_text, f_uris, img_uris = llm_client.respond_stream(
                latest_message=user_msg,
                with_media=True,
                fermion__is_fermion_supervised=process_log_streaming_enabled,
                fermion__export_type=APIExportTypesNames.ASSISTANT,
                fermion__endpoint=endpoint
            )

            MultimodalChatMessage.objects.create(
                multimodal_chat=api_chat,
                sender_type='ASSISTANT',
                message_text_content=llm_response_text
            )

        except Exception as e:

            logger.error(f"Internal server error: {str(e)}")
            return JsonResponse(
                {
                    "message": "Internal server error: " + str(e),
                    "data": {},
                    "status": ExportAPIStatusCodes.INTERNAL_SERVER_ERROR
                },
                status=ExportAPIStatusCodes.INTERNAL_SERVER_ERROR
            )

        resp_data = {
            "message": "Success",
            "data": {
                "metadata": {
                    "organization": {
                        "organization_name": export_assistant.assistant.organization.name,
                    },
                    "assistant": {
                        "assistant_name": export_assistant.assistant.name,
                        "assistant_description": export_assistant.assistant.description,
                    },
                    "chat": {
                        "chat_name": api_chat.chat_name,
                    }
                },
                "message": {
                    "assistant_name": export_assistant.assistant.name,
                    "content": llm_response_text,
                    "role": "assistant",
                    "media": {
                        "files": f_uris,
                        "images": img_uris
                    }
                }
            }
        }

        logger.info(f"Export Assistant API response: {resp_data}")
        return JsonResponse(resp_data, status=ExportAPIStatusCodes.OK)
