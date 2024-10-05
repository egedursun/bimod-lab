#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: endpoint_export_orchestration_views.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:44
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
#  File: endpoint_export_orchestration_views.py
#  Last Modified: 2024-09-28 15:08:41
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:53:00
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps._services.orchestration.orchestration_executor import OrchestrationExecutor
from apps.export_orchestrations.models import ExportOrchestrationAPI, OrchestratorRequestLog
from apps.export_orchestrations.utils import StatusCodes
from apps.orchestrations.models import OrchestrationQuery, OrchestrationQueryLog
from apps.orchestrations.utils import OrchestrationQueryLogTypesNames
from config.settings import BASE_URL


@method_decorator(csrf_exempt, name='dispatch')
class ExportOrchestrationAPIView(View):
    def post(self, request, *args, **kwargs):
        endpoint = BASE_URL + request.path
        api_key = request.headers.get('Authorization')
        try:
            export_assistant: ExportOrchestrationAPI = ExportOrchestrationAPI.objects.get(endpoint=endpoint)

        # Endpoint existence control
        except ExportOrchestrationAPI.DoesNotExist:
            return JsonResponse({
                "message": "Invalid endpoint", "data": {}, "status": StatusCodes.NOT_FOUND
            }, status=StatusCodes.NOT_FOUND)

        # Check if the endpoint is active
        if not export_assistant.is_online:
            return JsonResponse({
                "message": "The endpoint is currently offline. Please try again later.", "data": {},
                "status": StatusCodes.SERVICE_OFFLINE
            }, status=StatusCodes.SERVICE_OFFLINE)

        # API key correctness control
        if (not export_assistant.is_public) and export_assistant.custom_api_key != api_key:
            return JsonResponse({
                "message": "The API key provided is invalid, please provide a valid API key.", "data": {},
                "status": StatusCodes.UNAUTHORIZED
            }, status=StatusCodes.UNAUTHORIZED)

        # add the RequestLog
        OrchestratorRequestLog.objects.create(export_orchestration=export_assistant)
        # Request limit control
        if export_assistant.requests_in_last_hour() > export_assistant.request_limit_per_hour:
            return JsonResponse({
                "error": "The API request limit has been reached. Please try again later.",
                "data": {
                    "request_limit_per_hour": export_assistant.request_limit_per_hour,
                    "requests_in_last_hour": export_assistant.requests_in_last_hour()
                },
            }, status=StatusCodes.TOO_MANY_REQUESTS)

        body = json.loads(request.body)
        try:
            chat_history = body.get('chat_history')
            if len(chat_history) == 0:
                raise ValueError("Chat history is empty.")
            if "role" not in chat_history[0]:
                raise ValueError("Each of the chat history elements must contain 'role' key, which can either"
                                 "be 'system', 'assistant' or 'user'.")
            if chat_history[0]["role"] not in ["system", "assistant", "user"]:
                raise ValueError("The 'role' key in the first element of the chat history must be either 'system',"
                                 "'assistant' or 'user'.")
            if "content" not in chat_history[0]:
                raise ValueError("Each of the chat history elements must contain 'content' key.")
            # if content is not a string or is empty, raise an error
            if not isinstance(chat_history[0]["content"], str):
                raise ValueError("The 'content' key in the first element of the chat history must be a string.")
        except Exception as e:
            return JsonResponse({
                "message": "Internal server error: " + str(e), "data": {}, "status": StatusCodes.INTERNAL_SERVER_ERROR
            }, status=StatusCodes.INTERNAL_SERVER_ERROR)

        # Add the user messages to the chat
        user_message = None
        api_chat: OrchestrationQuery = None
        try:
            for message in chat_history:
                role = message["role"]
                if not role:
                    print("[ExportOrchestrationAPIView.post] Role is not provided in the chat history.")
                content = message["content"]
                file_uris = message.get("file_uris") or []
                image_uris = message.get("image_uris") or []
                if not file_uris or not image_uris:
                    print("[ExportOrchestrationAPIView.post] File or image URIs are not provided in the chat history.")
                user_message = content
                # Create a chat that's associated with the user
                api_chat: OrchestrationQuery = OrchestrationQuery.objects.create(
                    maestro=export_assistant.orchestrator,
                    query_text=user_message,
                    created_by_user=export_assistant.created_by_user,
                    last_updated_by_user=export_assistant.created_by_user)
                query_log = OrchestrationQueryLog.objects.create(
                    orchestration_query=api_chat,
                    log_type=OrchestrationQueryLogTypesNames.USER,
                    log_text_content=content,
                    log_file_contents=None,
                    log_image_contents=None,
                )
                api_chat.logs.add(query_log)
                api_chat.save()

        except Exception as e:
            return JsonResponse({
                "message": "Internal server error: " + str(e), "data": {}, "status": StatusCodes.INTERNAL_SERVER_ERROR
            }, status=StatusCodes.INTERNAL_SERVER_ERROR)

        try:
            orchestration_executor = OrchestrationExecutor(
                maestro=export_assistant.orchestrator,
                query_chat=api_chat
            )
            final_response = orchestration_executor.execute_for_query()
        except Exception as e:
            return JsonResponse({
                "message": "Internal server error: " + str(e), "data": {}, "status": StatusCodes.INTERNAL_SERVER_ERROR
            }, status=StatusCodes.INTERNAL_SERVER_ERROR)

        # Implement the logic for the assistant's response
        response_data = {"message": "Success", "data": {
            "metadata": {"organization": {"organization_name": export_assistant.orchestrator.organization.name, },
                         "assistant": {"assistant_name": export_assistant.orchestrator.name}},
            "message": {"assistant_name": export_assistant.orchestrator.name, "content": final_response,
                        "role": "assistant", "media": {"files": [], "images": []}
                        }}}
        return JsonResponse(response_data, status=StatusCodes.OK)
