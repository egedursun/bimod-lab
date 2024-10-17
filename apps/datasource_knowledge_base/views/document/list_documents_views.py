#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_knowledge_base.models import DocumentKnowledgeBaseConnection, KnowledgeBaseDocument, \
    DocumentProcessingLog
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DocumentView_List(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_KNOWLEDGE_BASE_DOCS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_KNOWLEDGE_BASE_DOCS):
            messages.error(self.request, "You do not have permission to list Knowledge Base documents.")
            return context
        ##############################

        orgs = Organization.objects.filter(users__in=[request.user])
        data = []
        for org in orgs:
            agents = Assistant.objects.filter(organization=org)
            agent_data_list = []
            for agent in agents:
                vector_stores = DocumentKnowledgeBaseConnection.objects.filter(assistant=agent)
                kb_data_list = []
                for kb in vector_stores:
                    docs = KnowledgeBaseDocument.objects.filter(knowledge_base=kb).order_by('-created_at')
                    paginator = Paginator(docs, 5)  # 5 documents per page
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    doc_data_list = []
                    for doc in page_obj:
                        log_entries = DocumentProcessingLog.objects.filter(document_full_uri=doc.document_uri)
                        proc_statuses = [log.log_message for log in log_entries]
                        doc_data_list.append({'document': doc, 'current_statuses': proc_statuses})
                    kb_data_list.append({
                        'knowledge_base': kb, 'documents': page_obj, 'document_data': doc_data_list,
                    })
                agent_data_list.append({'assistant': agent, 'knowledge_bases': kb_data_list})
            data.append({'organization': org, 'assistants': agent_data_list})

        context['data'] = data
        context['document_statuses'] = ['staged', 'uploaded', 'loaded', 'chunked', 'embedded_document',
                                        'saved_document', 'processed_document', 'embedded_chunks', 'saved_chunks',
                                        'processed_chunks', 'completed']
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

        doc_ids = request.POST.getlist('selected_documents')
        if doc_ids:
            KnowledgeBaseDocument.objects.filter(id__in=doc_ids).delete()
            messages.success(request, 'Selected documents deleted successfully.')
        return redirect('datasource_knowledge_base:list_documents')
