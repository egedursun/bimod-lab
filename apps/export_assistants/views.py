"""
This module contains views for managing Export Assistant APIs within the Bimod.io platform.

The views handle creating, updating, deleting, and listing Export Assistant APIs, as well as processing requests to these APIs. These views are restricted to authenticated users with the appropriate permissions and involve various checks to ensure security, such as API key validation, request limits, and endpoint availability.
"""

import importlib
import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, DeleteView

from apps._services.llms.llm_decoder import InternalLLMClient
from apps.assistants.models import Assistant
from apps.export_assistants.management.commands.start_exported_assistants import start_endpoint_for_assistant
from apps.export_assistants.models import ExportAssistantAPI, RequestLog
from apps.multimodal_chat.models import MultimodalChat, ChatSourcesNames, MultimodalChatMessage
from apps.multimodal_chat.utils import generate_chat_name
from apps.organization.models import Organization
from apps.user_permissions.models import UserPermission, PermissionNames
from config import settings
from config.settings import MAX_ASSISTANT_EXPORTS_ORGANIZATION, BASE_URL, EXPORT_API_BASE_URL
from web_project import TemplateLayout


class StatusCodes:
    """
    A simple class containing HTTP status codes used throughout the views.

    Attributes:
        OK (int): HTTP 200 OK.
        NOT_FOUND (int): HTTP 404 Not Found.
        UNAUTHORIZED (int): HTTP 401 Unauthorized.
        TOO_MANY_REQUESTS (int): HTTP 429 Too Many Requests.
        SERVICE_OFFLINE (int): HTTP 503 Service Unavailable.
        INTERNAL_SERVER_ERROR (int): HTTP 500 Internal Server Error.
    """
    OK = 200
    NOT_FOUND = 404
    UNAUTHORIZED = 401
    TOO_MANY_REQUESTS = 429
    SERVICE_OFFLINE = 503
    INTERNAL_SERVER_ERROR = 500


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


class ListExportAssistantsView(TemplateView, LoginRequiredMixin):
    """
    Displays a list of all Export Assistant APIs created by the user.

    This view retrieves all exported assistants associated with the user's organizations and displays them along with usage statistics.

    Methods:
        get_context_data(self, **kwargs): Retrieves the exported assistants and usage statistics for the user's organizations and adds them to the context.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user_context = self.request.user
        max_export_assistants = settings.MAX_ASSISTANT_EXPORTS_ORGANIZATION
        organization_data = []
        organizations = Organization.objects.filter(users=user_context)

        for organization in organizations:
            export_assistants_count = organization.exported_assistants.count()
            assistants_percentage = round((export_assistants_count / max_export_assistants) * 100, 2)
            export_assistants = organization.exported_assistants.all()
            for assistant in export_assistants:
                assistant.usage_percentage = 100  # Set this to actual percentage if needed
            organization_data.append({
                'organization': organization, 'export_assistants_count': export_assistants_count,
                'assistants_percentage': assistants_percentage, 'export_assistants': export_assistants,
                'limit': max_export_assistants
            })
        export_assistants = ExportAssistantAPI.objects.filter(created_by_user=user_context)
        context["user"] = user_context
        context["organization_data"] = organization_data
        context["export_assistants"] = export_assistants
        return context


class CreateExportAssistantsView(TemplateView, LoginRequiredMixin):
    """
    Handles the creation of a new Export Assistant API.

    This view allows users with the appropriate permissions to create a new Export Assistant API, associate it with an assistant, and set various properties such as request limits and public availability.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with available assistants and other necessary data.
        post(self, request, *args, **kwargs): Processes the form submission for creating a new Export Assistant API, including permission checks and validation.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user_context = self.request.user
        assistants = Assistant.objects.filter(organization__users=user_context)
        context["user"] = user_context
        context["assistants"] = assistants
        return context

    def post(self, request, *args, **kwargs):
        assistant_id = request.POST.get('assistant')
        assistant = get_object_or_404(Assistant, pk=assistant_id)
        is_public = request.POST.get('is_public') == 'on'
        request_limit_per_hour = request.POST.get('request_limit_per_hour')
        context_user = request.user

        # PERMISSION CHECK FOR - EXPORT_ASSISTANTS/CREATE
        user_permissions = UserPermission.active_permissions.filter(user=context_user).all().values_list(
            'permission_type', flat=True
        )
        if PermissionNames.ADD_EXPORT_ASSISTANT not in user_permissions:
            messages.error(request, "You do not have permission to create assistant exports.")
            return redirect('export_assistants:list')

        # check if the number of assistants of the organization is higher than the allowed limit
        if ExportAssistantAPI.objects.filter(
            created_by_user=request.user).count() > MAX_ASSISTANT_EXPORTS_ORGANIZATION:
            messages.error(request, f"Maximum number of Export Assistant APIs reached for the organization.")
            return self.render_to_response(self.get_context_data())

        if not assistant_id or not request_limit_per_hour:
            messages.error(request, "Assistant ID and Request Limit Per Hour are required.")
            return self.render_to_response(self.get_context_data())

        try:
            new_export_assistant = ExportAssistantAPI.objects.create(
                assistant_id=assistant_id, is_public=is_public, request_limit_per_hour=request_limit_per_hour,
                created_by_user=request.user
            )
            # Add the exported assistant to organization
            organization = assistant.organization
            organization.exported_assistants.add(new_export_assistant)
            organization.save()
            # Start the endpoint immediately
            start_endpoint_for_assistant(assistant=new_export_assistant)
            messages.success(request, "Export Assistant API created successfully!")
            print("[CreateExportAssistantsView.post] Export Assistant API created successfully!")
            return redirect("export_assistants:list")
        except Exception as e:
            messages.error(request, f"Error creating Export Assistant API: {str(e)}")
            return self.render_to_response(self.get_context_data())


class UpdateExportAssistantsView(TemplateView, LoginRequiredMixin):
    """
    Handles updating an existing Export Assistant API.

    This view allows users with the appropriate permissions to modify an existing Export Assistant API's attributes, such as request limits and public availability.

    Methods:
        get_context_data(self, **kwargs): Retrieves the current Export Assistant API details and adds them to the context, along with other relevant data such as available assistants.
        post(self, request, *args, **kwargs): Processes the form submission for updating the Export Assistant API, including permission checks and validation.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        export_assistant = get_object_or_404(ExportAssistantAPI, pk=self.kwargs['pk'])
        context['export_assistant'] = export_assistant
        context['assistants'] = Assistant.objects.all()  # Assuming you have an Assistant model
        return context

    def post(self, request, *args, **kwargs):
        export_assistant = get_object_or_404(ExportAssistantAPI, pk=self.kwargs['pk'])
        context_user = request.user
        # PERMISSION CHECK FOR - EXPORT_ASSISTANTS/UPDATE
        user_permissions = UserPermission.active_permissions.filter(user=context_user).all().values_list(
            'permission_type', flat=True
        )
        if PermissionNames.UPDATE_EXPORT_ASSIST not in user_permissions:
            messages.error(request, "You do not have permission to update assistant exports.")
            return redirect('export_assistants:list')

        export_assistant.assistant_id = request.POST.get('assistant')
        export_assistant.request_limit_per_hour = request.POST.get('request_limit_per_hour')
        export_assistant.is_public = request.POST.get('is_public') == 'on'
        if export_assistant.assistant_id and export_assistant.request_limit_per_hour:
            export_assistant.save()
            messages.success(request, "Export Assistant updated successfully.")
            print("[UpdateExportAssistantsView.post] Export Assistant updated successfully!")
            return redirect('export_assistants:list')
        else:
            messages.error(request, "There was an error updating the Export Assistant.")

        context = {
            'export_assistant': export_assistant, 'assistants': Assistant.objects.all()
        }
        return render(request, self.template_name, context)


class DeleteExportAssistantsView(LoginRequiredMixin, DeleteView):
    """
    Handles the deletion of an Export Assistant API.

    This view allows users with the appropriate permissions to delete an Export Assistant API and remove it from the associated organization.

    Methods:
        post(self, request, *args, **kwargs): Deletes the Export Assistant API if the user has the required permissions.
    """

    model = ExportAssistantAPI
    success_url = 'export_assistants:list'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        context_user = request.user
        export_assistant = get_object_or_404(ExportAssistantAPI, id=self.kwargs['pk'])
        # PERMISSION CHECK FOR - EXPORT_ASSISTANTS/DELETE
        user_permissions = UserPermission.active_permissions.filter(user=context_user).all().values_list(
            'permission_type', flat=True
        )
        if PermissionNames.DELETE_EXPORT_ASSISTANT not in user_permissions:
            messages.error(request, "You do not have permission to delete assistant exports.")
            return redirect('export_assistants:list')

        export_assistant.delete()
        success_message = "Export Assistant deleted successfully."
        # remove the exported assistant from the organization
        organization = export_assistant.assistant.organization
        organization.exported_assistants.remove(export_assistant)
        organization.save()
        print("[DeleteExportAssistantsView.post] Export Assistant deleted successfully.")
        messages.success(request, success_message)
        return redirect(self.success_url)


class ToggleExportAssistantServiceView(LoginRequiredMixin, View):
    """
    Toggles the online/offline status of an Export Assistant API.

    This view allows users with the appropriate permissions to toggle an Export Assistant API's availability by either starting or pausing its endpoint.

    Methods:
        post(self, request, *args, **kwargs): Toggles the assistant's online status and starts or stops the endpoint accordingly.
    """

    def post(self, request, *args, **kwargs):
        export_assistant = get_object_or_404(ExportAssistantAPI, pk=self.kwargs['pk'])
        endpoint = EXPORT_API_BASE_URL + export_assistant.endpoint.split(EXPORT_API_BASE_URL)[1]
        context_user = request.user
        # PERMISSION CHECK FOR - EXPORT_ASSISTANTS/UPDATE
        user_permissions = UserPermission.active_permissions.filter(user=context_user).all().values_list(
            'permission_type', flat=True
        )
        if PermissionNames.UPDATE_EXPORT_ASSIST not in user_permissions:
            messages.error(request, "You do not have permission to update assistant exports.")
            return redirect('export_assistants:list')

        api_urls = getattr(importlib.import_module(settings.ROOT_URLCONF), 'urlpatterns')
        export_assistant.is_online = not export_assistant.is_online
        export_assistant.save()

        # Pause or start the endpoint based on the assistant's new online status
        if export_assistant.is_online:
            # check if the endpoint is already in the url patterns
            if not any(endpoint in str(url) for url in api_urls):
                start_endpoint_for_assistant(export_assistant)
        return redirect('export_assistants:list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
