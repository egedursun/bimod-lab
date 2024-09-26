from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.organization.models import Organization
from apps.user_permissions.models import PermissionNames
from web_project import TemplateLayout


class ListAssistantView(LoginRequiredMixin, TemplateView):
    """
    Displays a list of assistants associated with the user's organizations.

    This view retrieves all assistants that belong to the organizations the user is a part of and displays them in a list. Currently, all authenticated users are allowed to view the list of assistants.

    Methods:
        get_context_data(self, **kwargs): Retrieves the assistants for the user's organizations and adds them to the context.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - LIST_ASSISTANTS
        if not UserPermissionManager.is_authorized(user=user, operation=PermissionNames.LIST_ASSISTANTS):
            messages.error(self.request, "You do not have permission to list assistants.")
            return context
        ##############################

        organizations = Organization.objects.filter(users__in=[user])
        org_assistants = {org: org.assistants.all() for org in organizations}
        context['org_assistants'] = org_assistants
        return context
