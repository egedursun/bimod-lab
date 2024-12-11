#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_knowledge_base_views.py
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

from apps.datasource_knowledge_base.models import (
    DocumentKnowledgeBaseConnection
)

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class VectorStoreView_Delete(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        context['knowledge_base'] = DocumentKnowledgeBaseConnection.objects.get(
            pk=self.kwargs['pk']
        )

        return context

    def post(self, request, *args, **kwargs):
        vector_store = DocumentKnowledgeBaseConnection.objects.get(
            pk=self.kwargs['pk']
        )

        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - DELETE_KNOWLEDGE_BASES
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_KNOWLEDGE_BASES
        ):
            messages.error(self.request, "You do not have permission to delete Knowledge Bases.")
            return redirect('datasource_knowledge_base:list')
        ##############################

        try:
            vector_store.delete()

        except Exception as e:
            logger.error(f"User: {context_user} - Knowledge Base - Delete Error: {e}")
            messages.error(request, 'An error occurred while deleting the knowledge base.')

            return redirect('datasource_knowledge_base:list')

        logger.info(f"[views.delete_knowledge_base] Knowledge Base deleted successfully.")
        messages.success(request, "Knowledge Base deleted successfully.")

        return redirect('datasource_knowledge_base:list')
