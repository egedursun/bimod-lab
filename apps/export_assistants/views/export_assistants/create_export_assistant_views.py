from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.user_permissions.models import PermissionNames
from config.settings import MAX_ASSISTANT_EXPORTS_ORGANIZATION
from web_project import TemplateLayout


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
        from apps.export_assistants.models import ExportAssistantAPI
        from apps.export_assistants.management.commands.start_exported_assistants import start_endpoint_for_assistant

        ##############################
        # PERMISSION CHECK FOR - ADD_EXPORT_ASSISTANT
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_EXPORT_ASSISTANT):
            messages.error(self.request, "You do not have permission to add Export Assistant APIs.")
            return redirect('export_assistants:list')
        ##############################

        assistant_id = request.POST.get('assistant')
        assistant = get_object_or_404(Assistant, pk=assistant_id)
        is_public = request.POST.get('is_public') == 'on'
        request_limit_per_hour = request.POST.get('request_limit_per_hour')

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
