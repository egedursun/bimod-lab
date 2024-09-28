from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_knowledge_base.forms import DocumentKnowledgeBaseForm
from apps.datasource_knowledge_base.utils import KNOWLEDGE_BASE_SYSTEMS, VECTORIZERS
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DocumentKnowledgeBaseCreateView(LoginRequiredMixin, TemplateView):
    """
    Handles the creation of new document knowledge base connections.

    This view displays a form for creating a new knowledge base connection. Upon submission, it validates the input, checks user permissions, and saves the new connection to the database. If the user lacks the necessary permissions, an error message is displayed.

    Methods:
        get_context_data(self, **kwargs): Adds additional context to the template, including available knowledge base systems, vectorizers, and assistants.
        post(self, request, *args, **kwargs): Handles form submission and knowledge base connection creation, including permission checks and validation.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        context['user'] = context_user
        context['knowledge_base_systems'] = KNOWLEDGE_BASE_SYSTEMS
        context['vectorizers'] = VECTORIZERS
        user_organizations = context_user.organizations.all()
        assistants_of_organizations = Assistant.objects.filter(organization__in=user_organizations)
        context['assistants'] = assistants_of_organizations
        context['form'] = DocumentKnowledgeBaseForm()
        return context

    def post(self, request, *args, **kwargs):
        form = DocumentKnowledgeBaseForm(request.POST)
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - ADD_KNOWLEDGE_BASES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_KNOWLEDGE_BASES):
            messages.error(self.request, "You do not have permission to create Knowledge Bases.")
            return redirect('datasource_knowledge_base:list')
        ##############################

        if form.is_valid():
            form.save()
            messages.success(request, "Knowledge Base created successfully.")
            print('[DocumentKnowledgeBaseCreateView.post] Knowledge Base created successfully.')
            return redirect('datasource_knowledge_base:list')
        else:
            messages.error(request,
                           "Error creating Knowledge Base. Please check the form for errors: %s" % form.errors)
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)
