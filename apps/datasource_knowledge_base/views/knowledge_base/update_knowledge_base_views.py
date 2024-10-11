#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: update_knowledge_base_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:47
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_knowledge_base.forms import DocumentKnowledgeBaseForm
from apps.datasource_knowledge_base.models import DocumentKnowledgeBaseConnection
from apps.datasource_knowledge_base.utils import VECTORSTORE_SYSTEMS, EMBEDDING_VECTORIZER_MODELS
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class VectorStoreView_Update(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        vector_store = get_object_or_404(DocumentKnowledgeBaseConnection, pk=kwargs['pk'])
        context['user'] = context_user
        context['knowledge_base_systems'] = VECTORSTORE_SYSTEMS
        context['vectorizers'] = EMBEDDING_VECTORIZER_MODELS
        user_orgs = context_user.organizations.all()
        agents_of_orgs = Assistant.objects.filter(organization__in=user_orgs)
        context['assistants'] = agents_of_orgs
        context['connection'] = vector_store
        context['form'] = DocumentKnowledgeBaseForm(instance=vector_store)
        return context

    def post(self, request, *args, **kwargs):
        vector_store = get_object_or_404(DocumentKnowledgeBaseConnection, pk=kwargs['pk'])

        ##############################
        # PERMISSION CHECK FOR - ADD_KNOWLEDGE_BASES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_KNOWLEDGE_BASES):
            messages.error(self.request, "You do not have permission to update Knowledge Bases.")
            return redirect('datasource_knowledge_base:list')
        ##############################

        form = DocumentKnowledgeBaseForm(request.POST, instance=vector_store)
        if form.is_valid():
            form.save()
            messages.success(request, "Knowledge Base updated successfully.")
            return redirect('datasource_knowledge_base:list')
        else:
            messages.error(request, "Error updating Knowledge Base. Please check the form for errors.")
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)
