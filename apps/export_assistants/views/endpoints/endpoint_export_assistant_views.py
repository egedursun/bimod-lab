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

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.core.generative_ai.generative_ai_decode_manager import GenerativeAIDecodeController
from apps.export_assistants.models import ExportAssistantAPI, RequestLog
from apps.export_assistants.utils import ExportAPIStatusCodes
from apps.multimodal_chat.models import MultimodalChat, MultimodalChatMessage
from apps.multimodal_chat.utils import generate_chat_name, SourcesForMultimodalChatsNames
from config.settings import BASE_URL


logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class ExportAssistantAPIView(View):
    def post(self, request, *args, **kwargs):
        endpoint = BASE_URL + request.path
        api_key = request.headers.get('Authorization')

        try:
            export_assistant = ExportAssistantAPI.objects.get(endpoint=endpoint)
        except ExportAssistantAPI.DoesNotExist:
            logger.error(f"Invalid endpoint: {endpoint}")
            return JsonResponse({
                "message": "Invalid endpoint", "data": {}, "status": ExportAPIStatusCodes.NOT_FOUND
            }, status=ExportAPIStatusCodes.NOT_FOUND)

        if not export_assistant.is_online:
            logger.error(f"The endpoint is currently offline: {endpoint}")
            return JsonResponse({
                "message": "The endpoint is currently offline. Please try again later.", "data": {},
                "status": ExportAPIStatusCodes.SERVICE_OFFLINE
            }, status=ExportAPIStatusCodes.SERVICE_OFFLINE)

        if (not export_assistant.is_public) and export_assistant.custom_api_key != api_key:
            logger.error(f"Invalid API key provided for endpoint: {endpoint}")
            return JsonResponse({
                "message": "The API key provided is invalid, please provide a valid API key.", "data": {},
                "status": ExportAPIStatusCodes.UNAUTHORIZED
            }, status=ExportAPIStatusCodes.UNAUTHORIZED)

        RequestLog.objects.create(export_assistant=export_assistant)
        if export_assistant.requests_in_last_hour() > export_assistant.request_limit_per_hour:
            logger.error(f"The API request limit has been reached for endpoint: {endpoint}")
            return JsonResponse({
                "error": "The API request limit has been reached. Please try again later.",
                "data": {
                    "request_limit_per_hour": export_assistant.request_limit_per_hour,
                    "requests_in_last_hour": export_assistant.requests_in_last_hour()
                },
            }, status=ExportAPIStatusCodes.TOO_MANY_REQUESTS)

        body = json.loads(request.body)
        try:
            chat_history = body.get('chat_history')
            if len(chat_history) == 0:
                logger.error(f"Invalid chat history provided for endpoint: {endpoint}")
                raise ValueError("Chat history is empty.")
            if "role" not in chat_history[0]:
                logger.error(f"Invalid chat history provided for endpoint: {endpoint}")
                raise ValueError("Each of the chat history elements must contain 'role' key, which can either"
                                 "be 'system', 'assistant' or 'user'.")
            if chat_history[0]["role"] not in ["system", "assistant", "user"]:
                logger.error(f"Invalid chat history provided for endpoint: {endpoint}")
                raise ValueError("The 'role' key in the first element of the chat history must be either 'system',"
                                 "'assistant' or 'user'.")
            if "content" not in chat_history[0]:
                logger.error(f"Invalid chat history provided for endpoint: {endpoint}")
                raise ValueError("Each of the chat history elements must contain 'content' key.")
            if not isinstance(chat_history[0]["content"], str):
                logger.error(f"Invalid chat history provided for endpoint: {endpoint}")
                raise ValueError("The 'content' key in the first element of the chat history must be a string.")
        except Exception as e:
            logger.error(f"Invalid chat history provided for endpoint: {endpoint}")
            return JsonResponse({
                "message": "Internal server error: " + str(e), "data": {}, "status": ExportAPIStatusCodes.INTERNAL_SERVER_ERROR
            }, status=ExportAPIStatusCodes.INTERNAL_SERVER_ERROR)

        api_chat = MultimodalChat.objects.create(
            organization=export_assistant.assistant.organization, assistant=export_assistant.assistant,
            user=export_assistant.created_by_user, chat_name=generate_chat_name(),
            created_by_user=export_assistant.created_by_user, chat_source=SourcesForMultimodalChatsNames.API)

        user_msg = None
        try:
            for msg in chat_history:
                role = msg["role"]
                content = msg["content"]
                f_uris = msg.get("file_uris") or []
                img_uris = msg.get("image_uris") or []
                api_chat.chat_messages.create(
                    multimodal_chat=api_chat, sender_type=role.upper(), message_text_content=content,
                    message_file_contents=f_uris, message_image_contents=img_uris
                )
                user_msg = api_chat.chat_messages.filter(sender_type=role.upper()).last()

        except Exception as e:
            logger.error(f"Invalid chat history provided for endpoint: {endpoint}")
            return JsonResponse({
                "message": "Internal server error: " + str(e),
                "data": {}, "status": ExportAPIStatusCodes.INTERNAL_SERVER_ERROR
            }, status=ExportAPIStatusCodes.INTERNAL_SERVER_ERROR)

        try:
            llm_client = GenerativeAIDecodeController.get(assistant=export_assistant.assistant, multimodal_chat=api_chat)
            llm_response_text, f_uris, img_uris = llm_client.respond(latest_message=user_msg, with_media=True)
            MultimodalChatMessage.objects.create(
                multimodal_chat=api_chat, sender_type='ASSISTANT', message_text_content=llm_response_text
            )
        except Exception as e:
            logger.error(f"Internal server error: {str(e)}")
            return JsonResponse({
                "message": "Internal server error: " + str(e), "data": {}, "status": ExportAPIStatusCodes.INTERNAL_SERVER_ERROR
            }, status=ExportAPIStatusCodes.INTERNAL_SERVER_ERROR)

        resp_data = {"message": "Success", "data": {
            "metadata": {"organization": {"organization_name": export_assistant.assistant.organization.name, },
                         "assistant": {"assistant_name": export_assistant.assistant.name,
                                       "assistant_description": export_assistant.assistant.description, },
                         "chat": {"chat_name": api_chat.chat_name, }},
            "message": {"assistant_name": export_assistant.assistant.name, "content": llm_response_text,
                        "role": "assistant", "media": {"files": f_uris, "images": img_uris}
                        }}}
        logger.info(f"Export Assistant API response: {resp_data}")
        return JsonResponse(resp_data, status=ExportAPIStatusCodes.OK)
