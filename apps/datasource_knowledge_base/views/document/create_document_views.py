#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#

import io
import logging
import uuid

import boto3
from django.contrib import messages

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.shortcuts import redirect

from django.views.generic import (
    TemplateView
)

from slugify import slugify

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.assistants.models import (
    Assistant
)

from apps.datasource_knowledge_base.models import (
    DocumentKnowledgeBaseConnection,
    KnowledgeBaseDocument
)

from apps.datasource_knowledge_base.tasks.document.embed_document_item_tasks import (
    load_and_index_document
)

from apps.datasource_knowledge_base.utils import (
    generate_document_uri
)

from apps.organization.models import (
    Organization
)

from apps.user_permissions.utils import (
    PermissionNames
)

from config import settings
from config.settings import MEDIA_URL
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class DocumentView_Create(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        user_agents = Assistant.objects.filter(
            organization__users__in=[request.user]
        )

        vector_stores = DocumentKnowledgeBaseConnection.objects.filter(
            assistant__in=user_agents
        )

        orgs = Organization.objects.filter(
            users__in=[request.user]
        )

        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        context['organizations'] = list(
            orgs.values(
                'id',
                'name'
            )
        )

        context['assistants'] = list(
            user_agents.values(
                'id',
                'name',
                'organization_id'
            )
        )

        context['knowledge_bases'] = list(
            vector_stores.values(
                'id',
                'name',
                'assistant_id'
            )
        )

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        vs_id = request.POST.get('knowledge_base') or None

        ##############################
        # PERMISSION CHECK FOR - ADD_KNOWLEDGE_BASE_DOCS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.ADD_KNOWLEDGE_BASE_DOCS
        ):
            messages.error(self.request, "You do not have permission to add Knowledge Base documents.")
            return redirect('datasource_knowledge_base:list_documents')
        ##############################

        if not vs_id:
            logger.error('Please select a knowledge base.')
            messages.error(request, 'Please select a knowledge base.')

            return redirect('datasource_knowledge_base:create_documents')

        try:
            vector_store = DocumentKnowledgeBaseConnection.objects.get(
                pk=vs_id
            )

            fs = request.FILES.getlist('document_files')

            if vs_id and fs:

                agent_base_dir = vector_store.assistant.document_base_directory
                f_paths = []
                document_items = []

                for file in fs:
                    file_type = file.name.split('.')[-1]
                    structured_file_name = slugify(file.name) + f"_{str(uuid.uuid4()).replace('-', '')}"

                    doc_uri = generate_document_uri(
                        agent_base_dir,
                        structured_file_name,
                        file_type
                    )

                    f_paths.append(doc_uri)

                    bucket = settings.AWS_STORAGE_BUCKET_NAME
                    bucket_path = f"{doc_uri.split(MEDIA_URL)[1]}"

                    file.seek(0)

                    file_buffer = io.BytesIO(
                        file.read()
                    )

                    s3_client = boto3.client("s3")

                    file_buffer.seek(0)

                    s3_client.upload_fileobj(
                        file_buffer,
                        bucket,
                        bucket_path
                    )

                    # Save the object item
                    new_document = KnowledgeBaseDocument.objects.create(
                        knowledge_base=vector_store,
                        document_type=file_type,
                        document_file_name=structured_file_name,
                        document_uri=doc_uri,
                        created_by_user=request.user
                    )
                    new_document.save()

                    document_items.append(new_document)

                    logger.info(f"Document uploaded: {structured_file_name}")

                # Handle document indexing process
                success = load_and_index_document(
                    items=document_items
                )

                if not success:
                    logger.error('Error while indexing documents.')
                    messages.error(request, 'Error while indexing documents.')

                logger.info('Documents uploaded successfully.')
                messages.success(request, 'Documents uploaded successfully.')

                return redirect('datasource_knowledge_base:list_documents')

            else:
                logger.error('Please select a knowledge base and upload documents.')
                messages.error(request, 'Please select a knowledge base and upload documents.')

        except Exception as e:
            logger.error(f"Error while uploading documents: {e}")
            messages.error(request, f"Error while uploading documents: {e}")

        return redirect('datasource_knowledge_base:create_documents')
