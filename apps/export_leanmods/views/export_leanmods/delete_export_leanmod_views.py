from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DeleteView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.export_leanmods.models import ExportLeanmodAssistantAPI
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DeleteExportLeanmodAssistantsView(LoginRequiredMixin, DeleteView):
    model = ExportLeanmodAssistantAPI
    success_url = 'export_leanmods:list'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - DELETE_EXPORT_LEANMOD
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_EXPORT_LEANMOD):
            messages.error(self.request, "You do not have permission to delete Export LeanMod Assistant APIs.")
            return redirect('export_leanmods:list')
        ##############################

        export_assistant = get_object_or_404(ExportLeanmodAssistantAPI, id=self.kwargs['pk'])
        export_assistant.delete()
        success_message = "Export LeanMod Assistant deleted successfully."
        # remove the exported assistant from the organization
        organization = export_assistant.lean_assistant.organization
        organization.exported_leanmods.remove(export_assistant)
        organization.save()
        print("[DeleteExportLeanmodAssistantsView.post] Export Assistant deleted successfully.")
        messages.success(request, success_message)
        return redirect(self.success_url)
