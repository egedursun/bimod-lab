from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.orchestrations.models import Maestro
from apps.organization.models import Organization
from apps.user_permissions.models import PermissionNames
from web_project import TemplateLayout


class OrchestrationListView(LoginRequiredMixin, TemplateView):
    """
    Displays a list of orchestrations within the Bimod.io platform.

    This view displays a list of orchestrations that the user has access to. It organizes the orchestrations
    by organization.
    """
    template_name = 'orchestrations/list_orchestrations.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_ORCHESTRATIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_ORCHESTRATIONS):
            messages.error(self.request, "You do not have permission to list orchestrations.")
            return context
        ##############################

        user_organizations = Organization.objects.filter(users__in=[self.request.user])
        orchestrations = Maestro.objects.filter(organization__in=user_organizations)

        # Organizing orchestrations by organization
        orchestrations_by_org = {}
        for org in user_organizations:
            orchestrations_by_org[org] = orchestrations.filter(organization=org)

        context['orchestrations_by_organization'] = orchestrations_by_org
        return context
