#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_all_documents_views.py
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
    KnowledgeBaseDocument
)

from apps.datasource_knowledge_base.tasks import (
    handle_delete_document_item
)

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class DocumentView_DeleteAll(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):
        context = self.post(request, *args, **kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - DELETE_KNOWLEDGE_BASE_DOCS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_KNOWLEDGE_BASE_DOCS
        ):
            messages.error(self.request, "You do not have permission to delete Knowledge Base documents.")
            return redirect('datasource_knowledge_base:list_documents')
        ##############################

        try:
            vs_id = kwargs.get('kb_id')

            docs = KnowledgeBaseDocument.objects.filter(
                knowledge_base_id=vs_id
            )

            for doc in docs:
                doc: KnowledgeBaseDocument

                success = handle_delete_document_item(
                    item=doc
                )

                if success is False:
                    logger.error(f"An error occurred while deleting the data for Document item with ID: {doc.id}")
                    messages.error(request, 'An error occurred while deleting all documents.')

                    continue

        except Exception as e:
            logger.error(f"User: {request.user} - Document - Delete All Error: {e}")
            messages.error(request, 'An error occurred while deleting all documents.')

            return redirect('datasource_knowledge_base:list_documents')

        messages.success(
            request,
            'All documents in the selected knowledge base have been deleted successfully.'
        )

        logger.info(
            f"[views.delete_all_documents] All documents in the selected knowledge base have been deleted successfully."
        )

        return redirect('datasource_knowledge_base:list_documents')
