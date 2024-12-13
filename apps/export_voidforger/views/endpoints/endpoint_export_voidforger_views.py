#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: endpoint_export_voidforger_views.py
#  Last Modified: 2024-11-24 21:36:17
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-24 21:53:05
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

from django.utils.decorators import (
    method_decorator
)

from django.views import View

from django.views.decorators.csrf import (
    csrf_exempt
)

from apps.core.generative_ai.generative_ai_decode_manager import (
    GenerativeAIDecodeController
)

from apps.export_voidforger.models import (
    ExportVoidForgerAPI,
    VoidForgerRequestLog
)

from apps.export_voidforger.utils import (
    ExportVoidForgerRequestStatusCodes
)

from apps.multimodal_chat.utils import (
    generate_chat_name,
    SourcesForMultimodalChatsNames
)

from apps.voidforger.models import (
    MultimodalVoidForgerChat,
    MultimodalVoidForgerChatMessage
)

from config.consumers import (
    APIExportTypesNames
)

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class ExportVoidForgerAPIStatusView(View):
    def get(self, request, *args, **kwargs):
        endpoint = request.path

        pattern = r'^/app/export_voidforger/status/voidforger_assistants/(?P<organization_id>\d+)/(?P<assistant_id>\d+)/(?P<export_id>\d+)/$'
        match = re.match(pattern, endpoint)

        if match:
            export_id = int(match.group('export_id'))

        else:

            return JsonResponse(
                {
                    "message": "Invalid path parameters.",
                    "data": {},
                    "status": ExportVoidForgerRequestStatusCodes.NOT_FOUND
                },
                status=ExportVoidForgerRequestStatusCodes.NOT_FOUND
            )

        api_key = request.headers.get('Authorization', None)
        if api_key and "Bearer" in api_key:
            api_key = api_key.replace("Bearer ", "").strip()

        try:
            export_assistant: ExportVoidForgerAPI = ExportVoidForgerAPI.objects.get(
                id=export_id
            )

        except ExportVoidForgerAPI.DoesNotExist:
            logger.error(f"Invalid VoidForger endpoint: {endpoint}")

            return JsonResponse(
                {
                    "message": "Invalid VoidForger endpoint",
                    "data": {},
                    "status": ExportVoidForgerRequestStatusCodes.NOT_FOUND
                },
                status=ExportVoidForgerRequestStatusCodes.NOT_FOUND
            )

        if (not export_assistant.is_public) and export_assistant.custom_api_key != api_key:
            logger.error(f"Invalid VoidForger API key provided for endpoint: {endpoint}")

        return JsonResponse(
            {
                "message": "The VoidForger API key provided is invalid, please provide a valid API key.",
                "data": {},
                "status": ExportVoidForgerRequestStatusCodes.UNAUTHORIZED
            },
            status=ExportVoidForgerRequestStatusCodes.UNAUTHORIZED
        )

        if not export_assistant.is_online:
            logger.error(f"The VoidForger endpoint is currently offline: {endpoint}")
            return JsonResponse(
                {
                    "message": "The VoidForger endpoint is currently offline. Please try again later.",
                    "data": {},
                    "status": ExportVoidForgerRequestStatusCodes.SERVICE_OFFLINE
                },
                status=ExportVoidForgerRequestStatusCodes.SERVICE_OFFLINE
            )

        VoidForgerRequestLog.objects.create(
            export_voidforger=export_assistant
        )

        if export_assistant.requests_in_last_hour() > export_assistant.request_limit_per_hour:
            logger.error(f"The VoidForger API request limit has been reached for endpoint: {endpoint}")

            return JsonResponse(
                {
                    "error": "The VoidForger API request limit has been reached. Please try again later.",
                    "data": {
                        "request_limit_per_hour": export_assistant.request_limit_per_hour,
                        "requests_in_last_hour": export_assistant.requests_in_last_hour()
                    },
                },
                status=ExportVoidForgerRequestStatusCodes.TOO_MANY_REQUESTS
            )

        status_data = export_assistant.voidforger.runtime_status
        instructions = export_assistant.voidforger.additional_instructions
        max_actions_per_cycle = export_assistant.voidforger.maximum_actions_per_cycle

        current_cycle = export_assistant.voidforger.auto_run_current_cycle
        max_lifetime_cycles = export_assistant.voidforger.auto_run_max_lifetime_cycles
        auto_run_trigger_interval_minutes = export_assistant.voidforger.auto_run_trigger_interval_minutes

        return JsonResponse(
            {
                "message": "The VoidForger status information has been retrieved successfully.",
                "data": {
                    "status": status_data,
                    "instructions": instructions,
                    "maximum_actions_per_cycle": max_actions_per_cycle,
                    "current_cycle": current_cycle,
                    "max_lifetime_cycles": max_lifetime_cycles,
                    "auto_run_trigger_interval_minutes": auto_run_trigger_interval_minutes
                },
                "status": ExportVoidForgerRequestStatusCodes.OK
            },
            status=ExportVoidForgerRequestStatusCodes.OK
        )

    def post(self, request, *args, **kwargs):
        endpoint = request.path

        pattern = r'^/app/export_voidforger/status/voidforger_assistants/(?P<organization_id>\d+)/(?P<assistant_id>\d+)/(?P<export_id>\d+)/$'
        match = re.match(pattern, endpoint)

        if match:
            export_id = int(match.group('export_id'))

        else:

            return JsonResponse(
                {
                    "message": "Invalid path parameters.",
                    "data": {},
                    "status": ExportVoidForgerRequestStatusCodes.NOT_FOUND
                },
                status=ExportVoidForgerRequestStatusCodes.NOT_FOUND
            )

        try:
            export_assistant = ExportVoidForgerAPI.objects.get(
                id=export_id
            )

        except ExportVoidForgerAPI.DoesNotExist:
            return JsonResponse(
                {
                    "message": "Invalid VoidForger endpoint",
                    "data": {},
                    "status": ExportVoidForgerRequestStatusCodes.NOT_FOUND
                },
                status=ExportVoidForgerRequestStatusCodes.NOT_FOUND
            )

        api_key = request.headers.get('Authorization', None)
        if api_key and "Bearer" in api_key:
            api_key = api_key.replace("Bearer ", "").strip()

        try:
            export_assistant: ExportVoidForgerAPI = ExportVoidForgerAPI.objects.get(
                id=export_id
            )

        except ExportVoidForgerAPI.DoesNotExist:
            logger.error(f"Invalid VoidForger endpoint: {endpoint}")

            return JsonResponse(
                {
                    "message": "Invalid VoidForger endpoint",
                    "data": {},
                    "status": ExportVoidForgerRequestStatusCodes.NOT_FOUND
                },
                status=ExportVoidForgerRequestStatusCodes.NOT_FOUND
            )

        if (not export_assistant.is_public) and export_assistant.custom_api_key != api_key:
            logger.error(f"Invalid VoidForger API key provided for endpoint: {endpoint}")

        return JsonResponse(
            {
                "message": "The VoidForger API key provided is invalid, please provide a valid API key.",
                "data": {},
                "status": ExportVoidForgerRequestStatusCodes.UNAUTHORIZED
            },
            status=ExportVoidForgerRequestStatusCodes.UNAUTHORIZED
        )

        if not export_assistant.is_online:
            logger.error(f"The VoidForger endpoint is currently offline: {endpoint}")
            return JsonResponse(
                {
                    "message": "The VoidForger endpoint is currently offline. Please try again later.",
                    "data": {},
                    "status": ExportVoidForgerRequestStatusCodes.SERVICE_OFFLINE
                },
                status=ExportVoidForgerRequestStatusCodes.SERVICE_OFFLINE
            )

        VoidForgerRequestLog.objects.create(
            export_voidforger=export_assistant
        )

        if export_assistant.requests_in_last_hour() > export_assistant.request_limit_per_hour:
            logger.error(f"The VoidForger API request limit has been reached for endpoint: {endpoint}")

            return JsonResponse(
                {
                    "error": "The VoidForger API request limit has been reached. Please try again later.",
                    "data": {
                        "request_limit_per_hour": export_assistant.request_limit_per_hour,
                        "requests_in_last_hour": export_assistant.requests_in_last_hour()
                    },
                },
                status=ExportVoidForgerRequestStatusCodes.TOO_MANY_REQUESTS
            )

        try:
            body = json.loads(request.body)
        except Exception as e:
            logger.error(f"Invalid request body provided: {str(e)}")

            return JsonResponse(
                {
                    "message": "Invalid request body provided: " + str(e),
                    "data": {},
                    "status": ExportVoidForgerRequestStatusCodes.BAD_REQUEST
                },
                status=ExportVoidForgerRequestStatusCodes.BAD_REQUEST
            )

        old_status_data = export_assistant.voidforger.runtime_status
        old_instructions = export_assistant.voidforger.additional_instructions
        old_max_actions_per_cycle = export_assistant.voidforger.maximum_actions_per_cycle

        old_max_lifetime_cycles = export_assistant.voidforger.auto_run_max_lifetime_cycles
        old_auto_run_trigger_interval = export_assistant.voidforger.auto_run_trigger_interval_minutes

        new_status_data = body.get('status', None)
        new_instructions = body.get('instructions', None)
        new_max_actions_per_cycle = body.get('maximum_actions_per_cycle', None)

        new_max_lifetime_cycles = body.get('max_lifetime_cycles', None)
        new_auto_run_trigger_interval = body.get('auto_run_trigger_interval_minutes', None)

        try:
            if new_status_data is not None:
                export_assistant.voidforger.runtime_status = new_status_data

                if new_status_data == VoidForgerRuntimeStatusesNames.ACTIVE:
                    action_type = VoidForgerToggleAutoExecutionActionTypesNames.ACTIVATED
                    metadata = {
                        "message": "VoidForger activation has been triggered by manual user interference. Activated VoidForger auto-execution pipeline."
                    }

                elif new_status_data == VoidForgerRuntimeStatusesNames.PAUSED:
                    action_type = VoidForgerToggleAutoExecutionActionTypesNames.PAUSED
                    metadata = {
                        "message": "VoidForger de-activation has been triggered by manual user interference. Paused VoidForger auto-execution pipeline."
                    }

                else:
                    logger.error(f"Invalid VoidForger status provided: {new_status_data}")

                    return JsonResponse(
                        {
                            "message": "Invalid VoidForger status provided.",
                            "data": {},
                            "status": ExportVoidForgerRequestStatusCodes.BAD_REQUEST
                        },
                        status=ExportVoidForgerRequestStatusCodes.BAD_REQUEST
                    )

                try:
                    VoidForgerToggleAutoExecutionLog.objects.create(
                        voidforger=voidforger,
                        action_type=action_type,
                        metadata=metadata,
                        responsible_user=self.request.user
                    )

                except Exception as e:
                    logger.error(f"Error creating VoidForger toggle auto execution log: {str(e)}")

                    return JsonResponse(
                        {
                            "message": "Internal server error: " + str(e),
                            "data": {},
                            "status": ExportVoidForgerRequestStatusCodes.INTERNAL_SERVER_ERROR
                        },
                        status=ExportVoidForgerRequestStatusCodes.INTERNAL_SERVER_ERROR
                    )

                export_assistant.voidforger.save()

            if new_instructions is not None:
                export_assistant.voidforger.additional_instructions = new_instructions

            if new_max_actions_per_cycle is not None:
                export_assistant.voidforger.maximum_actions_per_cycle = new_max_actions_per_cycle

            if new_max_lifetime_cycles is not None:
                export_assistant.voidforger.auto_run_max_lifetime_cycles = new_max_lifetime_cycles

            if new_auto_run_trigger_interval is not None:
                export_assistant.voidforger.auto_run_trigger_interval_minutes = new_auto_run_trigger_interval

            logger.info(f"Updating status for endpoint: {endpoint}")

            export_assistant.voidforger.save()

        except Exception as e:
            logger.error(f"Error updating status for endpoint: {endpoint}")

            return JsonResponse(
                {
                    "message": "Internal server error: " + str(e),
                    "data": {},
                    "status": ExportVoidForgerRequestStatusCodes.INTERNAL_SERVER_ERROR
                },
                status=ExportVoidForgerRequestStatusCodes.INTERNAL_SERVER_ERROR
            )

        logger.info(f"Status updated successfully for endpoint: {endpoint}")

        return JsonResponse(
            {
                "message": "The VoidForger status information has been updated successfully.",
                "data": {
                    "previous": {
                        "status": old_status_data,
                        "instructions": old_instructions,
                        "maximum_actions_per_cycle": old_max_actions_per_cycle,
                        "max_lifetime_cycles": old_max_lifetime_cycles,
                        "auto_run_trigger_interval_minutes": old_auto_run_trigger_interval
                    },
                    "current": {
                        "status": new_status_data,
                        "instructions": new_instructions,
                        "maximum_actions_per_cycle": new_max_actions_per_cycle,
                        "max_lifetime_cycles": new_max_lifetime_cycles,
                        "auto_run_trigger_interval_minutes": new_auto_run_trigger_interval
                    },
                },
                "status": ExportVoidForgerRequestStatusCodes.OK
            },
            status=ExportVoidForgerRequestStatusCodes.OK
        )


@method_decorator(csrf_exempt, name='dispatch')
class ExportVoidForgerAPIManualTriggerView(View):
    def post(self, request, *args, **kwargs):
        endpoint = request.path

        pattern = r'^/app/export_voidforger/manual_trigger/voidforger_assistants/(?P<organization_id>\d+)/(?P<assistant_id>\d+)/(?P<export_id>\d+)/$'
        match = re.match(pattern, endpoint)

        if match:
            export_id = int(match.group('export_id'))

        else:

            return JsonResponse(
                {
                    "message": "Invalid path parameters.",
                    "data": {},
                    "status": ExportVoidForgerRequestStatusCodes.NOT_FOUND
                },
                status=ExportVoidForgerRequestStatusCodes.NOT_FOUND
            )

        api_key = request.headers.get('Authorization', None)

        if api_key and "Bearer" in api_key:
            api_key = api_key.replace("Bearer ", "").strip()

        try:
            export_assistant: ExportVoidForgerAPI = ExportVoidForgerAPI.objects.get(
                id=export_id
            )

        except ExportVoidForgerAPI.DoesNotExist:
            logger.error(f"Invalid VoidForger endpoint: {endpoint}")

            return JsonResponse(
                {
                    "message": "Invalid VoidForger endpoint",
                    "data": {},
                    "status": ExportVoidForgerRequestStatusCodes.NOT_FOUND
                },
                status=ExportVoidForgerRequestStatusCodes.NOT_FOUND
            )

        if (not export_assistant.is_public) and export_assistant.custom_api_key != api_key:
            logger.error(f"Invalid VoidForger API key provided for endpoint: {endpoint}")

        return JsonResponse(
            {
                "message": "The VoidForger API key provided is invalid, please provide a valid API key.",
                "data": {},
                "status": ExportVoidForgerRequestStatusCodes.UNAUTHORIZED
            },
            status=ExportVoidForgerRequestStatusCodes.UNAUTHORIZED
        )

        if not export_assistant.is_online:
            logger.error(f"The VoidForger endpoint is currently offline: {endpoint}")
            return JsonResponse(
                {
                    "message": "The VoidForger endpoint is currently offline. Please try again later.",
                    "data": {},
                    "status": ExportVoidForgerRequestStatusCodes.SERVICE_OFFLINE
                },
                status=ExportVoidForgerRequestStatusCodes.SERVICE_OFFLINE
            )

        VoidForgerRequestLog.objects.create(
            export_voidforger=export_assistant
        )

        if export_assistant.requests_in_last_hour() > export_assistant.request_limit_per_hour:
            logger.error(f"The VoidForger API request limit has been reached for endpoint: {endpoint}")

            return JsonResponse(
                {
                    "error": "The VoidForger API request limit has been reached. Please try again later.",
                    "data": {
                        "request_limit_per_hour": export_assistant.request_limit_per_hour,
                        "requests_in_last_hour": export_assistant.requests_in_last_hour()
                    },
                },
                status=ExportVoidForgerRequestStatusCodes.TOO_MANY_REQUESTS
            )

        try:
            voidforger_id = export_assistant.voidforger.id

            xc = VoidForgerExecutionManager(
                user=self.request.user,
                voidforger_id=voidforger_id
            )

            error = xc.run_cycle(
                trigger=VoidForgerModesNames.MANUAL
            )

            if error:
                return JsonResponse(
                    {
                        "message": "There has been an error triggering the VoidForger manual run and/or during the execution.",
                        "data": {
                            "voidforger_id": voidforger_id,
                            "error": str(error),
                        },
                        "status": ExportVoidForgerRequestStatusCodes.INTERNAL_SERVER_ERROR
                    },
                )

        except Exception as e:

            logger.error(f"Error triggering manual run for endpoint: {endpoint}")

            return JsonResponse(
                {
                    "message": "Internal server error: " + str(e),
                    "data": {},
                    "status": ExportVoidForgerRequestStatusCodes.INTERNAL_SERVER_ERROR
                },
                status=ExportVoidForgerRequestStatusCodes.INTERNAL_SERVER_ERROR
            )

        return JsonResponse(
            {
                "message": "The VoidForger manual trigger order has been delivered successfully.",
                "data": {},
                "status": ExportVoidForgerRequestStatusCodes.OK
            },
            status=ExportVoidForgerRequestStatusCodes.OK
        )


@method_decorator(csrf_exempt, name='dispatch')
class ExportVoidForgerAPIHealthCheckView(View):
    def post(self, request, *args, **kwargs):
        endpoint = request.path

        pattern = r'^/app/export_voidforger/health/voidforger_assistants/(?P<organization_id>\d+)/(?P<assistant_id>\d+)/(?P<export_id>\d+)/$'
        match = re.match(pattern, endpoint)

        if match:
            export_id = int(match.group('export_id'))

        else:

            return JsonResponse(
                {
                    "message": "Invalid path parameters.",
                    "data": {},
                    "status": ExportVoidForgerRequestStatusCodes.NOT_FOUND
                },
                status=ExportVoidForgerRequestStatusCodes.NOT_FOUND
            )

        try:
            export_assistant = ExportVoidForgerAPI.objects.get(
                id=export_id
            )

        except ExportVoidForgerAPI.DoesNotExist:
            return JsonResponse(
                {
                    "message": "Invalid VoidForger endpoint",
                    "data": {},
                    "status": ExportVoidForgerRequestStatusCodes.NOT_FOUND
                },
                status=ExportVoidForgerRequestStatusCodes.NOT_FOUND
            )

        if not export_assistant.is_online:
            logger.error(f"The VoidForger endpoint is currently offline: {endpoint}")

            return JsonResponse(
                {
                    "message": "The VoidForger endpoint is currently offline. Please try again later.",
                    "data": {},
                    "status": ExportVoidForgerRequestStatusCodes.SERVICE_OFFLINE
                },
                status=ExportVoidForgerRequestStatusCodes.SERVICE_OFFLINE
            )

        VoidForgerRequestLog.objects.create(
            export_voidforger=export_assistant
        )

        if export_assistant.requests_in_last_hour() > export_assistant.request_limit_per_hour:
            logger.error(f"The VoidForger API request limit has been reached for endpoint: {endpoint}")

            return JsonResponse(
                {
                    "error": "The VoidForger API request limit has been reached. Please try again later.",
                    "data": {
                        "request_limit_per_hour": export_assistant.request_limit_per_hour,
                        "requests_in_last_hour": export_assistant.requests_in_last_hour()
                    },
                },
                status=ExportVoidForgerRequestStatusCodes.TOO_MANY_REQUESTS
            )

        return JsonResponse(
            {
                "message": "The VoidForger endpoint is online and ready to serve requests.",
                "data": {},
                "status": ExportVoidForgerRequestStatusCodes.OK
            },
            status=ExportVoidForgerRequestStatusCodes.OK
        )


@method_decorator(csrf_exempt, name='dispatch')
class ExportVoidForgerAPIView(View):
    def post(self, request, *args, **kwargs):
        endpoint = request.path

        pattern = r'^/app/export_voidforger/exported/voidforger_assistants/(?P<organization_id>\d+)/(?P<assistant_id>\d+)/(?P<export_id>\d+)/$'
        match = re.match(pattern, endpoint)

        if match:
            export_id = int(match.group('export_id'))

        else:

            return JsonResponse(
                {
                    "message": "Invalid path parameters.",
                    "data": {},
                    "status": ExportVoidForgerRequestStatusCodes.NOT_FOUND
                },
                status=ExportVoidForgerRequestStatusCodes.NOT_FOUND
            )

        api_key = request.headers.get('Authorization', None)

        if api_key and "Bearer" in api_key:
            api_key = api_key.replace("Bearer ", "").strip()

        try:
            export_assistant: ExportVoidForgerAPI = ExportVoidForgerAPI.objects.get(
                id=export_id
            )

        except ExportVoidForgerAPI.DoesNotExist:
            logger.error(f"Invalid VoidForger endpoint: {endpoint}")

            return JsonResponse(
                {
                    "message": "Invalid VoidForger endpoint",
                    "data": {},
                    "status": ExportVoidForgerRequestStatusCodes.NOT_FOUND
                },
                status=ExportVoidForgerRequestStatusCodes.NOT_FOUND
            )

        if not export_assistant.is_online:
            logger.error(f"The VoidForger endpoint is currently offline: {endpoint}")

            return JsonResponse(
                {
                    "message": "The VoidForger endpoint is currently offline. Please try again later.",
                    "data": {},
                    "status": ExportVoidForgerRequestStatusCodes.SERVICE_OFFLINE
                },
                status=ExportVoidForgerRequestStatusCodes.SERVICE_OFFLINE
            )

        if (not export_assistant.is_public) and export_assistant.custom_api_key != api_key:
            logger.error(f"Invalid VoidForger API key provided for endpoint: {endpoint}")

            return JsonResponse(
                {
                    "message": "The VoidForger API key provided is invalid, please provide a valid API key.",
                    "data": {},
                    "status": ExportVoidForgerRequestStatusCodes.UNAUTHORIZED
                },
                status=ExportVoidForgerRequestStatusCodes.UNAUTHORIZED
            )

        VoidForgerRequestLog.objects.create(
            export_voidforger=export_assistant
        )

        if export_assistant.requests_in_last_hour() > export_assistant.request_limit_per_hour:
            logger.error(f"The VoidForger API request limit has been reached for endpoint: {endpoint}")

            return JsonResponse(
                {
                    "error": "The VoidForger API request limit has been reached. Please try again later.",
                    "data": {
                        "request_limit_per_hour": export_assistant.request_limit_per_hour,
                        "requests_in_last_hour": export_assistant.requests_in_last_hour()
                    },
                },
                status=ExportVoidForgerRequestStatusCodes.TOO_MANY_REQUESTS
            )

        body = json.loads(request.body)

        try:
            chat_history = body.get('chat_history', [])

            options = body.get('options', {})

            process_log_streaming_enabled = False

            if "streaming_options" in options:
                streaming_options = options.get("streaming_options", {})

                if "process_log_streaming" in streaming_options:

                    process_log_streaming_enabled = streaming_options.get(
                        "process_log_streaming",
                        False
                    )

                else:
                    pass

            else:
                pass

            if len(chat_history) == 0:
                logger.error("Chat history is empty.")
                raise ValueError("Chat history is empty.")

            api_chat = MultimodalVoidForgerChat.objects.create(
                voidforger=export_assistant.voidforger,
                user=export_assistant.created_by_user,
                chat_name=generate_chat_name(),
                created_by_user=export_assistant.created_by_user,
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

                file_uris = [
                    uri.strip() for uri in file_uris if uri.strip()
                ] if file_uris else []

                image_uris = [
                    uri.strip() for uri in image_uris if uri.strip()
                ]

                user_message = api_chat.voidforger_chat_messages.create(
                    multimodal_voidforger_chat=api_chat,
                    sender_type=role.upper(),
                    message_text_content=content,
                    message_file_contents=file_uris,
                    message_image_contents=image_uris
                )

        except Exception as e:
            logger.error(f"Invalid chat history provided: {str(e)}")

            return JsonResponse(
                {
                    "message": "Internal server error: " + str(e),
                    "data": {},
                    "status": ExportVoidForgerRequestStatusCodes.INTERNAL_SERVER_ERROR
                },
                status=ExportVoidForgerRequestStatusCodes.INTERNAL_SERVER_ERROR
            )

        try:
            llm_client = GenerativeAIDecodeController.get_voidforger(
                assistant=export_assistant.voidforger,
                multimodal_chat=api_chat,
                user=export_assistant.created_by_user
            )

            llm_response_text, file_uris, image_uris = llm_client.respond_stream(
                latest_message=user_message,
                with_media=True,
                fermion__is_fermion_supervised=process_log_streaming_enabled,
                fermion__export_type=APIExportTypesNames.VOIDFORGER,
                fermion__endpoint=endpoint
            )

            MultimodalVoidForgerChatMessage.objects.create(
                multimodal_voidforger_chat=api_chat,
                sender_type='ASSISTANT',
                message_text_content=llm_response_text
            )

        except Exception as e:
            logger.error(f"Error generating response for endpoint: {endpoint}")

            return JsonResponse(
                {
                    "message": "Internal server error: " + str(e),
                    "data": {},
                    "status": ExportVoidForgerRequestStatusCodes.INTERNAL_SERVER_ERROR
                },
                status=ExportVoidForgerRequestStatusCodes.INTERNAL_SERVER_ERROR
            )

        response_data = {
            "message": "Success",
            "data": {
                "metadata": {
                    "organization": {
                        "organization_name": export_assistant.voidforger.llm_model.organization.name
                    },
                    "assistant": {
                        "assistant_name": "VoidForger"
                    }
                },
                "message": {
                    "assistant_name": "VoidForger",
                    "content": llm_response_text,
                    "role": "assistant",
                    "media": {
                        "files": [],
                        "images": []
                    }
                }
            }
        }

        logger.info(f"VoidForger executed successfully for endpoint: {endpoint}")

        return JsonResponse(
            response_data,
            status=ExportVoidForgerRequestStatusCodes.OK
        )
