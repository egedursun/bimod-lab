#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: create_document_views.py
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

import boto3
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.knowledge_base.document.knowledge_base_decoder import KnowledgeBaseSystemDecoder
from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_knowledge_base.models import DocumentKnowledgeBaseConnection
from apps.datasource_knowledge_base.tasks import add_document_upload_log
from apps.datasource_knowledge_base.utils import generate_document_uri, DocumentUploadStatusNames
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from config import settings
from config.settings import MEDIA_URL
from web_project import TemplateLayout


class AddDocumentView(LoginRequiredMixin, TemplateView):
    """
    Handles uploading documents to a selected knowledge base.

    This view displays a form for selecting a knowledge base and uploading documents to it. Upon form submission, it validates the input, uploads the documents to the storage (e.g., S3), and logs the upload process. If the user lacks the necessary permissions, an error message is displayed.

    Methods:
        get(self, request, *args, **kwargs): Prepares the context with the available knowledge bases and assistants for document uploading.
        post(self, request, *args, **kwargs): Handles the document upload process, including validation, file storage, and logging.
    """

    def get(self, request, *args, **kwargs):
        user_assistants = Assistant.objects.filter(organization__users__in=[request.user])
        knowledge_bases = DocumentKnowledgeBaseConnection.objects.filter(assistant__in=user_assistants)
        organizations = Organization.objects.filter(users__in=[request.user])
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['organizations'] = list(organizations.values('id', 'name'))
        context['assistants'] = list(user_assistants.values('id', 'name', 'organization_id'))
        context['knowledge_bases'] = list(knowledge_bases.values('id', 'name', 'assistant_id'))
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        knowledge_base_id = request.POST.get('knowledge_base') or None
        context_user = request.user

        ##############################
        # PERMISSION CHECK FOR - ADD_KNOWLEDGE_BASE_DOCS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_KNOWLEDGE_BASE_DOCS):
            messages.error(self.request, "You do not have permission to add Knowledge Base documents.")
            return redirect('datasource_knowledge_base:list_documents')
        ##############################

        if not knowledge_base_id:
            messages.error(request, 'Please select a knowledge base.')
            return redirect('datasource_knowledge_base:create_documents')
        knowledge_base = DocumentKnowledgeBaseConnection.objects.get(pk=knowledge_base_id)
        files = request.FILES.getlist('document_files')
        if knowledge_base_id and files:
            assistant_base_directory = knowledge_base.assistant.document_base_directory
            file_paths = []
            for file in files:
                file_type = file.name.split('.')[-1]
                document_uri = generate_document_uri(assistant_base_directory, file.name, file_type)
                file_paths.append(document_uri)
                add_document_upload_log(document_full_uri=document_uri, log_name=DocumentUploadStatusNames.STAGED)
                # SAVE the File to s3
                boto3_client = boto3.client('s3')
                bucket_name = settings.AWS_STORAGE_BUCKET_NAME
                s3_path = f"{document_uri.split(MEDIA_URL)[1]}"
                boto3_client.put_object(Bucket=bucket_name, Key=s3_path, Body=file)
                add_document_upload_log(document_full_uri=document_uri, log_name=DocumentUploadStatusNames.UPLOADED)
            # handle the task asynchronously inside the knowledge base system
            KnowledgeBaseSystemDecoder.get(knowledge_base).index_documents(document_paths=file_paths)
            messages.success(request, 'Documents uploaded successfully.')
            print('[AddDocumentView.post] Documents uploaded successfully.')
            return redirect('datasource_knowledge_base:list_documents')
        else:
            messages.error(request, 'Please select a knowledge base and upload documents.')
        return redirect('datasource_knowledge_base:create_documents')
