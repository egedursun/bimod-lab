from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.datasource_knowledge_base.models import DocumentKnowledgeBaseConnection
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DocumentKnowledgeBaseListView(LoginRequiredMixin, TemplateView):
    """
    Displays a list of document knowledge base connections associated with the user's organizations and assistants.

    This view retrieves all knowledge base connections organized by organization and assistant, and displays them in a structured list.

    Attributes:
        template_name (str): The template used to render the knowledge base list.

    Methods:
        get_context_data(self, **kwargs): Retrieves the knowledge base connections organized by organization and assistant, and adds them to the context.
    """

    template_name = "datasource_knowledge_base/base/list_knowledge_bases.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_KNOWLEDGE_BASES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_KNOWLEDGE_BASES):
            messages.error(self.request, "You do not have permission to list Knowledge Bases.")
            return context
        ##############################

        context_user = self.request.user
        user_organizations = Organization.objects.filter(users__in=[context_user])

        connections_by_organization = {}
        for organization in user_organizations:
            assistants = organization.assistants.all()
            assistants_connections = {}
            for assistant in assistants:
                connections = DocumentKnowledgeBaseConnection.objects.filter(assistant=assistant)
                if connections.exists():
                    assistants_connections[assistant] = connections
            if assistants_connections:
                connections_by_organization[organization] = assistants_connections

        context['connections_by_organization'] = connections_by_organization
        context['user'] = context_user
        return context
