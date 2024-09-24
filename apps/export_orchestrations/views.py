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

from apps._services.orchestration.orchestration_executor import OrchestrationExecutor
from apps.export_orchestrations.management.commands.start_exported_orchestrations import \
    start_endpoint_for_orchestration
from apps.export_orchestrations.models import ExportOrchestrationAPI, OrchestratorRequestLog
from apps.orchestrations.models import Maestro, OrchestrationQuery, OrchestrationQueryLog, \
    OrchestrationQueryLogTypesNames
from apps.organization.models import Organization
from apps.user_permissions.models import UserPermission, PermissionNames
from config import settings
from config.settings import BASE_URL, MAX_ORCHESTRATIONS_EXPORTS_ORGANIZATION, EXPORT_ORCHESTRATION_API_BASE_URL
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
class ExportOrchestrationAPIView(View):
    def post(self, request, *args, **kwargs):
        endpoint = BASE_URL + request.path
        api_key = request.headers.get('Authorization')
        try:
            export_assistant:ExportOrchestrationAPI = ExportOrchestrationAPI.objects.get(endpoint=endpoint)

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
                content = message["content"]
                file_uris = message.get("file_uris") or []
                image_uris = message.get("image_uris") or []
                user_message = content
                # Create a chat that's associated with the user
                api_chat: OrchestrationQuery = OrchestrationQuery.objects.create(
                    maestro=export_assistant.orchestrator,
                    query_text=user_message,
                    created_by_user=export_assistant.created_by_user,
                    last_updated_by_user = export_assistant.created_by_user)
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
            final_response = orchestration_executor.execute_for_query(user_query=user_message)
        except Exception as e:
            return JsonResponse({
                "message": "Internal server error: " + str(e), "data": {}, "status": StatusCodes.INTERNAL_SERVER_ERROR
            }, status=StatusCodes.INTERNAL_SERVER_ERROR)

        # Implement the logic for the assistant's response
        response_data = {"message": "Success", "data": {
            "metadata": {"organization": {"organization_name": export_assistant.orchestrator.organization.name, },
                         "assistant": {"assistant_name": export_assistant.orchestrator.name }},
            "message": {"assistant_name": export_assistant.orchestrator.name, "content": final_response,
                        "role": "assistant", "media": {"files": [], "images": []}
                        }}}
        return JsonResponse(response_data, status=StatusCodes.OK)


class ListExportOrchestrationsView(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user_context = self.request.user
        max_export_assistants = MAX_ORCHESTRATIONS_EXPORTS_ORGANIZATION
        organization_data = []
        organizations = Organization.objects.filter(users=user_context)

        for organization in organizations:
            export_assistants_count = organization.exported_orchestrations.count()
            assistants_percentage = round((export_assistants_count / max_export_assistants) * 100, 2)
            export_assistants = organization.exported_orchestrations.all()
            for assistant in export_assistants:
                assistant.usage_percentage = 100  # Set this to actual percentage if needed
            organization_data.append({
                'organization': organization, 'export_assistants_count': export_assistants_count,
                'assistants_percentage': assistants_percentage, 'export_assistants': export_assistants,
                'limit': max_export_assistants
            })
        export_assistants = ExportOrchestrationAPI.objects.filter(created_by_user=user_context)
        context["user"] = user_context
        context["organization_data"] = organization_data
        context["export_assistants"] = export_assistants
        return context


class CreateExportOrchestrationView(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user_context = self.request.user
        assistants = Maestro.objects.filter(organization__users=user_context)
        context["user"] = user_context
        context["assistants"] = assistants
        return context

    def post(self, request, *args, **kwargs):
        assistant_id = request.POST.get('assistant')
        assistant = get_object_or_404(Maestro, pk=assistant_id)
        is_public = request.POST.get('is_public') == 'on'
        request_limit_per_hour = request.POST.get('request_limit_per_hour')
        context_user = request.user

        # PERMISSION CHECK FOR - EXPORT_ORCHESTRATIONS/CREATE
        user_permissions = UserPermission.active_permissions.filter(user=context_user).all().values_list(
            'permission_type', flat=True
        )
        if PermissionNames.ADD_EXPORT_ASSISTANT not in user_permissions:
            messages.error(request, "You do not have permission to create orchestration exports.")
            return redirect('export_orchestrations:list')

        # check if the number of assistants of the organization is higher than the allowed limit
        if ExportOrchestrationAPI.objects.filter(
            created_by_user=request.user).count() > MAX_ORCHESTRATIONS_EXPORTS_ORGANIZATION:
            messages.error(request, f"Maximum number of Export Orchestration APIs reached for the organization.")
            return self.render_to_response(self.get_context_data())

        if not assistant_id or not request_limit_per_hour:
            messages.error(request, "Orchestration Assistant ID and Request Limit Per Hour are required.")
            return self.render_to_response(self.get_context_data())

        try:
            new_export_assistant = ExportOrchestrationAPI.objects.create(
                orchestrator_id=assistant_id, is_public=is_public, request_limit_per_hour=request_limit_per_hour,
                created_by_user=request.user
            )
            # Add the exported orchestration to organization
            organization = assistant.organization
            if not organization.exported_orchestrations:
                organization.exported_orchestrations.set([new_export_assistant])
            else:
                organization.exported_orchestrations.add(new_export_assistant)
            organization.save()
            # Start the endpoint immediately
            start_endpoint_for_orchestration(assistant=new_export_assistant)
            messages.success(request, "Export Orchestration API created successfully!")
            print("[CreateExportOrchestrationsView.post] Export Orchestration API created successfully!")
            return redirect("export_orchestrations:list")
        except Exception as e:
            messages.error(request, f"Error creating Export Orchestration API: {str(e)}")
            return self.render_to_response(self.get_context_data())


class UpdateExportOrchestrationView(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        export_assistant = get_object_or_404(ExportOrchestrationAPI, pk=self.kwargs['pk'])
        context['export_assistant'] = export_assistant
        context['assistants'] = Maestro.objects.filter(
            organization__users__in=[self.request.user]
        )
        return context

    def post(self, request, *args, **kwargs):
        export_assistant = get_object_or_404(ExportOrchestrationAPI, pk=self.kwargs['pk'])
        export_assistant: ExportOrchestrationAPI
        context_user = request.user
        # PERMISSION CHECK FOR - EXPORT_ASSISTANTS/UPDATE
        user_permissions = UserPermission.active_permissions.filter(user=context_user).all().values_list(
            'permission_type', flat=True
        )
        if PermissionNames.UPDATE_EXPORT_ASSIST not in user_permissions:
            messages.error(request, "You do not have permission to update Orchestration exports.")
            return redirect('export_orchestrations:list')

        export_assistant.orchestrator_id = request.POST.get('assistant')
        export_assistant.request_limit_per_hour = request.POST.get('request_limit_per_hour')
        export_assistant.is_public = request.POST.get('is_public') == 'on'
        if export_assistant.orchestrator_id and export_assistant.request_limit_per_hour:
            export_assistant.save()
            messages.success(request, "Export Orchestration updated successfully.")
            print("[UpdateExportOrchestrationView.post] Export Orchestration updated successfully!")
            return redirect('export_orchestrations:list')
        else:
            messages.error(request, "There was an error updating the Export Orchestration.")

        context = self.get_context_data()
        context.update(
            {
                'export_assistant': export_assistant,
                'assistants': Maestro.objects.filter(organization__users__in=[self.request.user]).all()
            })
        return render(request, self.template_name, context)


class DeleteExportOrchestrationView(LoginRequiredMixin, DeleteView):
    model = ExportOrchestrationAPI
    success_url = 'export_orchestrations:list'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        context_user = request.user
        export_assistant = get_object_or_404(ExportOrchestrationAPI, id=self.kwargs['pk'])
        # PERMISSION CHECK FOR - EXPORT_ASSISTANTS/DELETE
        user_permissions = UserPermission.active_permissions.filter(user=context_user).all().values_list(
            'permission_type', flat=True
        )
        if PermissionNames.DELETE_EXPORT_ASSISTANT not in user_permissions:
            messages.error(request, "You do not have permission to delete Orchestration exports.")
            return redirect('export_orchestrations:list')

        export_assistant.delete()
        success_message = "Export Orchestration deleted successfully."
        # remove the exported assistant from the organization
        organization = export_assistant.orchestrator.organization
        organization.exported_orchestrations.remove(export_assistant)
        organization.save()
        print("[DeleteExportOrchestrationsView.post] Export Orchestration deleted successfully.")
        messages.success(request, success_message)
        return redirect(self.success_url)


class ToggleExportOrchestrationServiceView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        export_assistant = get_object_or_404(ExportOrchestrationAPI, pk=self.kwargs['pk'])
        endpoint = EXPORT_ORCHESTRATION_API_BASE_URL + export_assistant.endpoint.split(EXPORT_ORCHESTRATION_API_BASE_URL)[1]
        context_user = request.user
        # PERMISSION CHECK FOR - EXPORT_ASSISTANTS/UPDATE
        user_permissions = UserPermission.active_permissions.filter(user=context_user).all().values_list(
            'permission_type', flat=True
        )
        if PermissionNames.UPDATE_EXPORT_ASSIST not in user_permissions:
            messages.error(request, "You do not have permission to update Orchestration exports.")
            return redirect('export_orchestrations:list')

        api_urls = getattr(importlib.import_module(settings.ROOT_URLCONF), 'urlpatterns')
        export_assistant.is_online = not export_assistant.is_online
        export_assistant.save()

        # Pause or start the endpoint based on the assistant's new online status
        if export_assistant.is_online:
            # check if the endpoint is already in the url patterns
            if not any(endpoint in str(url) for url in api_urls):
                start_endpoint_for_orchestration(export_assistant)
        return redirect('export_orchestrations:list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
