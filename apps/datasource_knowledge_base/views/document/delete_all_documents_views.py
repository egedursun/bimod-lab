#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: delete_all_documents_views.py
#  Last Modified: 2024-09-28 00:53:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:45:37
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.datasource_knowledge_base.models import KnowledgeBaseDocument
from apps.user_permissions.models import UserPermission
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DeleteAllDocumentsView(LoginRequiredMixin, TemplateView):
    """
    Handles deleting all documents within a specific knowledge base.

    This view allows users with the appropriate permissions to delete all documents in a selected knowledge base. It ensures that the user has the necessary permissions before performing the deletion.

    Methods:
        get_context_data(self, **kwargs): Prepares the context for rendering the confirmation of the deletion.
        post(self, request, *args, **kwargs): Deletes all documents in the selected knowledge base if the user has the required permissions.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):
        context = self.post(request, *args, **kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - DELETE_KNOWLEDGE_BASE_DOCS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_KNOWLEDGE_BASE_DOCS):
            messages.error(self.request, "You do not have permission to delete Knowledge Base documents.")
            return redirect('datasource_knowledge_base:list_documents')
        ##############################

        knowledge_base_id = kwargs.get('kb_id')
        context_user = request.user

        # PERMISSION CHECK FOR - DOCUMENT / DELETE
        user_permissions = (UserPermission.active_permissions.filter(user=context_user)
                            .all().values_list('permission_type', flat=True))
        if PermissionNames.DELETE_KNOWLEDGE_BASES not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {"Permission Error": "You do not have permission to delete documents."}
            return self.render_to_response(context)

        KnowledgeBaseDocument.objects.filter(knowledge_base_id=knowledge_base_id).delete()
        messages.success(request, 'All documents in the selected knowledge base have been deleted successfully.')
        print(
            '[DeleteAllDocumentsView.post] All documents in the selected knowledge base have been deleted successfully.')
        return redirect('datasource_knowledge_base:list_documents')
