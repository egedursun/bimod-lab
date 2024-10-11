#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: create_document_views.py
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

import boto3
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.vector_operations.vector_document.vector_store_decoder import KnowledgeBaseSystemDecoder
from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_knowledge_base.models import DocumentKnowledgeBaseConnection
from apps.datasource_knowledge_base.tasks import add_vector_store_doc_loaded_log
from apps.datasource_knowledge_base.utils import generate_document_uri, VectorStoreDocProcessingStatusNames
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from config import settings
from config.settings import MEDIA_URL
from web_project import TemplateLayout


class DocumentView_Create(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        user_agents = Assistant.objects.filter(organization__users__in=[request.user])
        vector_stores = DocumentKnowledgeBaseConnection.objects.filter(assistant__in=user_agents)
        orgs = Organization.objects.filter(users__in=[request.user])
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['organizations'] = list(orgs.values('id', 'name'))
        context['assistants'] = list(user_agents.values('id', 'name', 'organization_id'))
        context['knowledge_bases'] = list(vector_stores.values('id', 'name', 'assistant_id'))
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        vs_id = request.POST.get('knowledge_base') or None

        ##############################
        # PERMISSION CHECK FOR - ADD_KNOWLEDGE_BASE_DOCS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_KNOWLEDGE_BASE_DOCS):
            messages.error(self.request, "You do not have permission to add Knowledge Base documents.")
            return redirect('datasource_knowledge_base:list_documents')
        ##############################

        if not vs_id:
            messages.error(request, 'Please select a knowledge base.')
            return redirect('datasource_knowledge_base:create_documents')

        vector_store = DocumentKnowledgeBaseConnection.objects.get(pk=vs_id)
        fs = request.FILES.getlist('document_files')
        if vs_id and fs:
            agent_base_dir = vector_store.assistant.document_base_directory
            f_paths = []
            for file in fs:
                file_type = file.name.split('.')[-1]
                doc_uri = generate_document_uri(agent_base_dir, file.name, file_type)
                f_paths.append(doc_uri)
                add_vector_store_doc_loaded_log(document_full_uri=doc_uri, log_name=VectorStoreDocProcessingStatusNames.STAGED)
                s3c = boto3.client('s3')
                bucket = settings.AWS_STORAGE_BUCKET_NAME
                bucket_path = f"{doc_uri.split(MEDIA_URL)[1]}"
                s3c.put_object(Bucket=bucket, Key=bucket_path, Body=file)
                add_vector_store_doc_loaded_log(document_full_uri=doc_uri, log_name=VectorStoreDocProcessingStatusNames.UPLOADED)

            KnowledgeBaseSystemDecoder.get(vector_store).index_documents(document_paths=f_paths)
            messages.success(request, 'Documents uploaded successfully.')
            return redirect('datasource_knowledge_base:list_documents')
        else:
            messages.error(request, 'Please select a knowledge base and upload documents.')
        return redirect('datasource_knowledge_base:create_documents')
