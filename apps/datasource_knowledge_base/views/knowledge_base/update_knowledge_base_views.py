#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: update_knowledge_base_views.py
#  Last Modified: 2024-09-28 00:53:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:45:44
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_knowledge_base.forms import DocumentKnowledgeBaseForm
from apps.datasource_knowledge_base.models import DocumentKnowledgeBaseConnection
from apps.datasource_knowledge_base.utils import KNOWLEDGE_BASE_SYSTEMS, VECTORIZERS
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DocumentKnowledgeBaseUpdateView(LoginRequiredMixin, TemplateView):
    """
    Handles updating an existing document knowledge base connection.

    This view allows users with the appropriate permissions to modify a knowledge base connection's attributes. It also handles the form submission and validation for updating the connection.

    Methods:
        get_context_data(self, **kwargs): Retrieves the current knowledge base connection details and adds them to the context, along with other relevant data such as available knowledge base systems, vectorizers, and assistants.
        post(self, request, *args, **kwargs): Handles form submission for updating the knowledge base connection, including permission checks and validation.
    """

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
        # PERMISSION CHECK FOR - ADD_KNOWLEDGE_BASES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_KNOWLEDGE_BASES):
            messages.error(self.request, "You do not have permission to update Knowledge Bases.")
            return redirect('datasource_knowledge_base:list')
        ##############################

        form = DocumentKnowledgeBaseForm(request.POST, instance=knowledge_base)
        if form.is_valid():
            form.save()
            messages.success(request, "Knowledge Base updated successfully.")
            print('[DocumentKnowledgeBaseUpdateView.post] Knowledge Base updated successfully.')
            return redirect('datasource_knowledge_base:list')
        else:
            messages.error(request, "Error updating Knowledge Base. Please check the form for errors.")
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)
