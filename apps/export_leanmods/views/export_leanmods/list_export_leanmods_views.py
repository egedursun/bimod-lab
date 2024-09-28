from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.export_leanmods.models import ExportLeanmodAssistantAPI
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from config import settings
from web_project import TemplateLayout


class ListExportLeanmodAssistantsView(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_EXPORT_LEANMOD
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_EXPORT_LEANMOD):
            messages.error(self.request, "You do not have permission to list Export LeanMod Assistant APIs.")
            return context
        ##############################

        user_context = self.request.user
        max_export_assistants = settings.MAX_LEANMODS_EXPORTS_ORGANIZATION
        organization_data = []
        organizations = Organization.objects.filter(users=user_context)

        for organization in organizations:
            export_assistants_count = organization.exported_leanmods.count()
            assistants_percentage = round((export_assistants_count / max_export_assistants) * 100, 2)
            export_assistants = organization.exported_leanmods.all()
            for assistant in export_assistants:
                assistant.usage_percentage = 100  # Set this to actual percentage if needed
            organization_data.append({
                'organization': organization, 'export_assistants_count': export_assistants_count,
                'assistants_percentage': assistants_percentage, 'export_assistants': export_assistants,
                'limit': max_export_assistants
            })
        export_assistants = ExportLeanmodAssistantAPI.objects.filter(created_by_user=user_context)
        context["user"] = user_context
        context["organization_data"] = organization_data
        context["export_assistants"] = export_assistants
        return context
