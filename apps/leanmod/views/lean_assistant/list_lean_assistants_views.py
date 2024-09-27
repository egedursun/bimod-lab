from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.organization.models import Organization
from apps.user_permissions.models import PermissionNames
from web_project import TemplateLayout


class ListLeanAssistantsView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_LEAN_ASSISTANT
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_LEAN_ASSISTANT):
            messages.error(self.request, "You do not have permission to list LeanMod assistants.")
            return context
        ##############################

        org_lean_assistants = {}
        organizations = Organization.objects.prefetch_related('lean_assistants').filter(
            users__in=[self.request.user]
        ).all()

        # Group lean assistants by organization
        for organization in organizations:
            org_lean_assistants[organization] = organization.lean_assistants.all()

        context['org_lean_assistants'] = org_lean_assistants
        return context
