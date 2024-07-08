import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, DeleteView

from apps._services.llms.llm_decoder import InternalLLMClient
from apps.assistants.models import Assistant
from apps.export_assistants.models import ExportAssistantAPI, RequestLog
from apps.multimodal_chat.models import MultimodalChat, ChatSourcesNames
from apps.multimodal_chat.utils import generate_chat_name
from web_project import TemplateLayout


# Create your views here.

class StatusCodes:
    OK = 200
    NOT_FOUND = 404
    UNAUTHORIZED = 401
    TOO_MANY_REQUESTS = 429
    INTERNAL_SERVER_ERROR = 500


@method_decorator(csrf_exempt, name='dispatch')
class ExportAssistantAPIView(View):

    def post(self, request, *args, **kwargs):
        endpoint = request.path.split('exported/')[1]
        print("endpoint: ", endpoint)
        api_key = request.headers.get('Authorization')
        try:
            export_assistant = ExportAssistantAPI.objects.get(endpoint=endpoint)

        # Endpoint existence control
        except ExportAssistantAPI.DoesNotExist:
            return JsonResponse({
                "message": "Invalid endpoint",
                "data": {},
                "status": StatusCodes.NOT_FOUND
            }, status=StatusCodes.NOT_FOUND)

        # API key correctness control
        if (not export_assistant.is_public) and export_assistant.custom_api_key != api_key:
            return JsonResponse({
                "message": "The API key provided is invalid, please provide a valid API key.",
                "data": {},
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
                "message": "Internal server error: " + str(e),
                "data": {},
                "status": StatusCodes.INTERNAL_SERVER_ERROR
            }, status=StatusCodes.INTERNAL_SERVER_ERROR)

        # Create a chat that's associated with the user
        api_chat = MultimodalChat.objects.create(
                organization=export_assistant.assistant.organization,
                assistant=export_assistant.assistant,
                user=export_assistant.created_by_user,
                chat_name= generate_chat_name(),
                created_by_user=export_assistant.created_by_user,
                chat_source=ChatSourcesNames.API)

        # Add the user messages to the chat
        try:
            for message in chat_history:
                role = message["role"]
                content = message["content"]
                api_chat.chat_messages.create(
                    multimodal_chat=api_chat,
                    sender_type=role.upper(),
                    message_text_content=content
                )
                # save the chat
                api_chat.save()
        except Exception as e:
            return JsonResponse({
                "message": "Internal server error: " + str(e),
                "data": {},
                "status": StatusCodes.INTERNAL_SERVER_ERROR
            }, status=StatusCodes.INTERNAL_SERVER_ERROR)

        llm_response_text = ""
        try:
            llm_client = InternalLLMClient.get(assistant=export_assistant.assistant, multimodal_chat=api_chat)
            llm_response_text = llm_client.respond()
        except Exception as e:
            return JsonResponse({
                "message": "Internal server error: " + str(e),
                "data": {},
                "status": StatusCodes.INTERNAL_SERVER_ERROR
            }, status=StatusCodes.INTERNAL_SERVER_ERROR)

        # Implement the logic for the assistant's response
        response_data = {
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
                    "role": "assistant"
                }
            }
        }
        return JsonResponse(response_data, status=StatusCodes.OK)


class ListExportAssistantsView(TemplateView, LoginRequiredMixin):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user_context = self.request.user
        context["user"] = user_context
        return context


class CreateExportAssistantsView(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user_context = self.request.user
        assistants = Assistant.objects.filter(organization__users=user_context)
        context["user"] = user_context
        context["assistants"] = assistants
        return context

    def post(self, request, *args, **kwargs):
        assistant_id = request.POST.get('assistant')
        is_public = request.POST.get('is_public') == 'on'
        request_limit_per_hour = request.POST.get('request_limit_per_hour')

        if not assistant_id or not request_limit_per_hour:
            messages.error(request, "Assistant ID and Request Limit Per Hour are required.")
            return self.render_to_response(self.get_context_data())

        try:
            ExportAssistantAPI.objects.create(
                assistant_id=assistant_id,
                is_public=is_public,
                request_limit_per_hour=request_limit_per_hour,
                created_by_user=request.user
            )
            messages.success(request, "Export Assistant API created successfully!")
            return redirect("export_assistants:list")
        except Exception as e:
            messages.error(request, f"Error creating Export Assistant API: {str(e)}")
            return self.render_to_response(self.get_context_data())


class UpdateExportAssistantsView(TemplateView, LoginRequiredMixin):
    pass


class DeleteExportAssistantsView(DeleteView, LoginRequiredMixin):
    pass
