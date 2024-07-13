from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, DeleteView

from apps.assistants.models import VECTORIZERS, Assistant
from apps.datasource_knowledge_base.forms import DocumentKnowledgeBaseForm
from apps.datasource_knowledge_base.models import KNOWLEDGE_BASE_SYSTEMS, DocumentKnowledgeBaseConnection
from apps.organization.models import Organization
from apps.user_permissions.models import UserPermission, PermissionNames
from web_project import TemplateLayout


# Create your views here.


# KNOWLEDGE BASE VIEWS


class DocumentKnowledgeBaseCreateView(LoginRequiredMixin, TemplateView):

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
        # PERMISSION CHECK FOR - KNOWLEDGE BASE / CREATE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.ADD_KNOWLEDGE_BASES not in user_permissions:
            messages.error(request, "You do not have permission to create Knowledge Bases.")
            return redirect('datasource_knowledge_base:list')
        ##############################

        if form.is_valid():
            form.save()
            messages.success(request, "Knowledge Base created successfully.")
            return redirect('datasource_knowledge_base:list')
        else:
            messages.error(request, "Error creating Knowledge Base. Please check the form for errors.")
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


class DocumentKnowledgeBaseListView(LoginRequiredMixin, TemplateView):
    template_name = "datasource_knowledge_base/base/list_knowledge_bases.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
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


class DocumentKnowledgeBaseUpdateView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        knowledge_base = get_object_or_404(DocumentKnowledgeBaseConnection, pk=kwargs['pk'])
        context['user'] = context_user
        context['knowledge_base_systems'] = KNOWLEDGE_BASE_SYSTEMS
        context['vectorizers'] = VECTORIZERS
        user_organizations = context_user.organizations.all()
        assistants_of_organizations = Assistant.objects.filter(organization__in=user_organizations)
        context['assistants'] = assistants_of_organizations
        context['connection'] = knowledge_base
        context['form'] = DocumentKnowledgeBaseForm(instance=knowledge_base)
        return context

    def post(self, request, *args, **kwargs):
        knowledge_base = get_object_or_404(DocumentKnowledgeBaseConnection, pk=kwargs['pk'])
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - KNOWLEDGE BASE / UPDATE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.UPDATE_KNOWLEDGE_BASES not in user_permissions:
            messages.error(request, "You do not have permission to update Knowledge Bases.")
            return redirect('datasource_knowledge_base:list')
        ##############################

        form = DocumentKnowledgeBaseForm(request.POST, instance=knowledge_base)
        if form.is_valid():
            form.save()
            messages.success(request, "Knowledge Base updated successfully.")
            return redirect('datasource_knowledge_base:list')
        else:
            messages.error(request, "Error updating Knowledge Base. Please check the form for errors.")
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


class DocumentKnowledgeBaseDeleteView(LoginRequiredMixin, DeleteView):
    model = DocumentKnowledgeBaseConnection
    success_url = '/app/datasource_knowledge_base/list/'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['knowledge_base'] = self.get_object()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - KNOWLEDGE BASE / DELETE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.DELETE_KNOWLEDGE_BASES not in user_permissions:
            messages.error(request, "You do not have permission to delete Knowledge Bases.")
            return redirect('datasource_knowledge_base:list')
        ##############################

        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        context_user = self.request.user
        return DocumentKnowledgeBaseConnection.objects.filter(assistant__organization__users__in=[context_user])


# ...


# DOCUMENT VIEWS


# ...



