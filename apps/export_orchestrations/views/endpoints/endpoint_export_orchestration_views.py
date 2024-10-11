#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: endpoint_export_orchestration_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:46
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#


import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.core.orchestration.orchestration_executor import OrchestrationExecutor
from apps.export_orchestrations.models import ExportOrchestrationAPI, OrchestratorRequestLog
from apps.export_orchestrations.utils import ExportOrchestrationRequestStatusCodes
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
        except ExportOrchestrationAPI.DoesNotExist:
            return JsonResponse({
                "message": "Invalid endpoint", "data": {}, "status": ExportOrchestrationRequestStatusCodes.NOT_FOUND
            }, status=ExportOrchestrationRequestStatusCodes.NOT_FOUND)

        if not export_assistant.is_online:
            return JsonResponse({
                "message": "The endpoint is currently offline. Please try again later.", "data": {},
                "status": ExportOrchestrationRequestStatusCodes.SERVICE_OFFLINE
            }, status=ExportOrchestrationRequestStatusCodes.SERVICE_OFFLINE)

        if (not export_assistant.is_public) and export_assistant.custom_api_key != api_key:
            return JsonResponse({
                "message": "The API key provided is invalid, please provide a valid API key.", "data": {},
                "status": ExportOrchestrationRequestStatusCodes.UNAUTHORIZED
            }, status=ExportOrchestrationRequestStatusCodes.UNAUTHORIZED)

        OrchestratorRequestLog.objects.create(export_orchestration=export_assistant)
        if export_assistant.requests_in_last_hour() > export_assistant.request_limit_per_hour:
            return JsonResponse({
                "error": "The API request limit has been reached. Please try again later.",
                "data": {
                    "request_limit_per_hour": export_assistant.request_limit_per_hour,
                    "requests_in_last_hour": export_assistant.requests_in_last_hour()
                },
            }, status=ExportOrchestrationRequestStatusCodes.TOO_MANY_REQUESTS)

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
            if not isinstance(chat_history[0]["content"], str):
                raise ValueError("The 'content' key in the first element of the chat history must be a string.")
        except Exception as e:
            return JsonResponse({
                "message": "Internal server error: " + str(e), "data": {},
                "status": ExportOrchestrationRequestStatusCodes.INTERNAL_SERVER_ERROR
            }, status=ExportOrchestrationRequestStatusCodes.INTERNAL_SERVER_ERROR)

        user_msg = None
        api_chat: OrchestrationQuery = None
        try:
            for msg in chat_history:
                role = msg["role"]
                if not role:
                    pass
                content = msg["content"]
                f_uris = msg.get("file_uris") or []
                img_uris = msg.get("image_uris") or []
                if not f_uris or not img_uris:
                    pass
                user_msg = content
                api_chat: OrchestrationQuery = OrchestrationQuery.objects.create(
                    maestro=export_assistant.orchestrator, query_text=user_msg,
                    created_by_user=export_assistant.created_by_user,
                    last_updated_by_user=export_assistant.created_by_user)
                query_log = OrchestrationQueryLog.objects.create(
                    orchestration_query=api_chat, log_type=OrchestrationQueryLogTypesNames.USER,
                    log_text_content=content, log_file_contents=None, log_image_contents=None,
                )
                api_chat.logs.add(query_log)
                api_chat.save()

        except Exception as e:
            return JsonResponse({
                "message": "Internal server error: " + str(e), "data": {},
                "status": ExportOrchestrationRequestStatusCodes.INTERNAL_SERVER_ERROR
            }, status=ExportOrchestrationRequestStatusCodes.INTERNAL_SERVER_ERROR)

        try:
            orch_xc = OrchestrationExecutor(maestro=export_assistant.orchestrator, query_chat=api_chat)
            final_output = orch_xc.execute_for_query()
        except Exception as e:
            return JsonResponse({
                "message": "Internal server error: " + str(e), "data": {},
                "status": ExportOrchestrationRequestStatusCodes.INTERNAL_SERVER_ERROR
            }, status=ExportOrchestrationRequestStatusCodes.INTERNAL_SERVER_ERROR)
        response_data = {"message": "Success", "data": {
            "metadata": {"organization": {"organization_name": export_assistant.orchestrator.organization.name, },
                         "assistant": {"assistant_name": export_assistant.orchestrator.name}},
            "message": {"assistant_name": export_assistant.orchestrator.name, "content": final_output,
                        "role": "assistant", "media": {"files": [], "images": []}
                        }}}
        return JsonResponse(response_data, status=ExportOrchestrationRequestStatusCodes.OK)
