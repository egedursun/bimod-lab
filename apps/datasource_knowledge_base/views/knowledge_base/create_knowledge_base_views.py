#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_knowledge_base_views.py
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
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging

from django.contrib import messages

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.assistants.models import Assistant

from apps.datasource_knowledge_base.forms import (
    DocumentKnowledgeBaseForm
)

from apps.datasource_knowledge_base.utils import (
    VECTORSTORE_SYSTEMS,
    EMBEDDING_VECTORIZER_MODELS
)

from apps.user_permissions.utils import (
    PermissionNames
)

from config.settings import (
    MAX_KNOWLEDGE_BASES_PER_ASSISTANT
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class VectorStoreView_Create(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        try:
            context_user = self.request.user
            context['user'] = context_user

            context['knowledge_base_systems'] = VECTORSTORE_SYSTEMS
            context['vectorizers'] = EMBEDDING_VECTORIZER_MODELS

            user_orgs = context_user.organizations.all()

            agents_of_orgs = Assistant.objects.filter(
                organization__in=user_orgs
            )

            context['assistants'] = agents_of_orgs
            context['form'] = DocumentKnowledgeBaseForm()

        except Exception as e:
            logger.error(f"User: {self.request.user} - Knowledge Base - Create Error: {e}")
            messages.error(self.request, 'An error occurred while creating the knowledge base.')

            return context

        return context

    def post(self, request, *args, **kwargs):
        form = DocumentKnowledgeBaseForm(request.POST)

        ##############################
        # PERMISSION CHECK FOR - ADD_KNOWLEDGE_BASES
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.ADD_KNOWLEDGE_BASES
        ):
            messages.error(self.request, "You do not have permission to create Knowledge Bases.")
            return redirect('datasource_knowledge_base:list')
        ##############################

        if form.is_valid():

            assistant = form.cleaned_data['assistant']

            n_knowledge_bases = assistant.documentknowledgebaseconnection_set.count()

            if n_knowledge_bases > MAX_KNOWLEDGE_BASES_PER_ASSISTANT:
                messages.error(
                    request,
                    f'Assistant has reached the maximum number of knowledge base connections ({MAX_KNOWLEDGE_BASES_PER_ASSISTANT}).'
                )

                return redirect('datasource_knowledge_base:create')

            form.save()

            logger.info(f"[views.create_knowledge_base] Knowledge Base created successfully.")
            messages.success(request, "Knowledge Base created successfully.")

            return redirect('datasource_knowledge_base:list')

        else:
            logger.error(
                f"[views.create_knowledge_base] Error creating Knowledge Base. Please check the form for errors: {form.errors}"
            )

            messages.error(
                request,
                "Error creating Knowledge Base. Please check the form for errors: %s" % form.errors
            )

            context = self.get_context_data(**kwargs)
            context['form'] = form

            return self.render_to_response(context)
