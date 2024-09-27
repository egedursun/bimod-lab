import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps._services.llms.llm_decoder import InternalLLMClient
from apps.export_assistants.models import ExportAssistantAPI, RequestLog
from apps.export_assistants.utils import StatusCodes
from apps.multimodal_chat.models import MultimodalChat, ChatSourcesNames, MultimodalChatMessage
from apps.multimodal_chat.utils import generate_chat_name
from config.settings import BASE_URL


@method_decorator(csrf_exempt, name='dispatch')
class ExportAssistantAPIView(View):
    """
    Handles API requests sent to the exported assistant's endpoint.

    This view processes POST requests to an assistant's exported API, validating the request, checking the API key, logging the request, and generating a response from the assistant based on the provided chat history.

    Methods:
        post(self, request, *args, **kwargs): Processes the POST request, validates it, and returns a response from the assistant.
    """

    def post(self, request, *args, **kwargs):
        endpoint = BASE_URL + request.path
        api_key = request.headers.get('Authorization')
        try:
            export_assistant = ExportAssistantAPI.objects.get(endpoint=endpoint)

        # Endpoint existence control
        except ExportAssistantAPI.DoesNotExist:
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
        RequestLog.objects.create(export_assistant=export_assistant)
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

        # Create a chat that's associated with the user
        api_chat = MultimodalChat.objects.create(
            organization=export_assistant.assistant.organization,
            assistant=export_assistant.assistant,
            user=export_assistant.created_by_user,
            chat_name=generate_chat_name(),
            created_by_user=export_assistant.created_by_user,
            chat_source=ChatSourcesNames.API)
        # Add the user messages to the chat
        user_message = None
        try:
            for message in chat_history:
                role = message["role"]
                content = message["content"]
                file_uris = message.get("file_uris") or []
                image_uris = message.get("image_uris") or []
                api_chat.chat_messages.create(
                    multimodal_chat=api_chat, sender_type=role.upper(), message_text_content=content,
                    message_file_contents=file_uris, message_image_contents=image_uris
                )
                user_message = api_chat.chat_messages.filter(sender_type=role.upper()).last()

        except Exception as e:
            return JsonResponse({
                "message": "Internal server error: " + str(e), "data": {}, "status": StatusCodes.INTERNAL_SERVER_ERROR
            }, status=StatusCodes.INTERNAL_SERVER_ERROR)

        try:
            llm_client = InternalLLMClient.get(assistant=export_assistant.assistant, multimodal_chat=api_chat)
            llm_response_text, file_uris, image_uris = llm_client.respond(latest_message=user_message, with_media=True)
            MultimodalChatMessage.objects.create(
                multimodal_chat=api_chat, sender_type='ASSISTANT', message_text_content=llm_response_text
            )
        except Exception as e:
            return JsonResponse({
                "message": "Internal server error: " + str(e), "data": {}, "status": StatusCodes.INTERNAL_SERVER_ERROR
            }, status=StatusCodes.INTERNAL_SERVER_ERROR)

        # Implement the logic for the assistant's response
        response_data = {"message": "Success", "data": {
            "metadata": {"organization": {"organization_name": export_assistant.assistant.organization.name, },
                         "assistant": {"assistant_name": export_assistant.assistant.name,
                                       "assistant_description": export_assistant.assistant.description, },
                         "chat": {"chat_name": api_chat.chat_name, }},
            "message": {"assistant_name": export_assistant.assistant.name, "content": llm_response_text,
                        "role": "assistant", "media": {"files": file_uris, "images": image_uris}
                        }}}
        return JsonResponse(response_data, status=StatusCodes.OK)
