#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: list_documents_views.py
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
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_knowledge_base.models import DocumentKnowledgeBaseConnection, KnowledgeBaseDocument, \
    DocumentProcessingLog
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class ListDocumentsView(LoginRequiredMixin, TemplateView):
    """
    Displays a list of documents associated with the user's knowledge bases.

    This view retrieves all documents within the user's knowledge bases, organized by organization and assistant. It also allows users to delete selected documents.

    Methods:
        get(self, request, *args, **kwargs): Retrieves the documents for the user's knowledge bases and adds them to the context, including pagination and status information.
        post(self, request, *args, **kwargs): Handles the deletion of selected documents.
    """

    def get(self, request, *args, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_KNOWLEDGE_BASE_DOCS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_KNOWLEDGE_BASE_DOCS):
            messages.error(self.request, "You do not have permission to list Knowledge Base documents.")
            return context
        ##############################

        organizations = Organization.objects.filter(users__in=[request.user])
        data = []
        for org in organizations:
            assistants = Assistant.objects.filter(organization=org)
            assistant_data_list = []
            for assistant in assistants:
                knowledge_bases = DocumentKnowledgeBaseConnection.objects.filter(assistant=assistant)
                kb_data_list = []
                for kb in knowledge_bases:
                    documents = KnowledgeBaseDocument.objects.filter(knowledge_base=kb).order_by('-created_at')
                    paginator = Paginator(documents, 5)  # 5 documents per page
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)

                    document_data_list = []
                    for document in page_obj:
                        log_entries = DocumentProcessingLog.objects.filter(document_full_uri=document.document_uri)
                        current_statuses = [log.log_message for log in log_entries]
                        document_data_list.append({'document': document, 'current_statuses': current_statuses})
                    kb_data_list.append({
                        'knowledge_base': kb, 'documents': page_obj, 'document_data': document_data_list,
                    })
                assistant_data_list.append({'assistant': assistant, 'knowledge_bases': kb_data_list})
            data.append({'organization': org, 'assistants': assistant_data_list})

        context['data'] = data
        context['document_statuses'] = [
            'staged', 'uploaded', 'loaded', 'chunked', 'embedded_document', 'saved_document', 'processed_document',
            'embedded_chunks', 'saved_chunks', 'processed_chunks', 'completed'
        ]
        context['failed_statuses'] = ['failed']
        context['partially_failed_statuses'] = ['partially_failed']
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - DELETE_KNOWLEDGE_BASE_DOCS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_KNOWLEDGE_BASE_DOCS):
            messages.error(self.request, "You do not have permission to delete Knowledge Base documents.")
            return redirect('datasource_knowledge_base:list_documents')
        ##############################

        document_ids = request.POST.getlist('selected_documents')
        if document_ids:
            KnowledgeBaseDocument.objects.filter(id__in=document_ids).delete()
            messages.success(request, 'Selected documents deleted successfully.')
            print('[ListDocumentsView.post] Selected documents deleted successfully.')
        return redirect('datasource_knowledge_base:list_documents')
