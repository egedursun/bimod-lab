#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: integrate_knowledge_bases_views.py
#  Last Modified: 2024-12-21 19:06:05
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-21 19:06:06
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
import os
import uuid
import zipfile
from tempfile import TemporaryDirectory

import boto3
import requests

from django.contrib import (
    messages
)

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.shortcuts import (
    redirect
)

from django.views import View
from slugify import slugify

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.datasource_knowledge_base.models import (
    DocumentKnowledgeBaseConnection,
    KnowledgeBaseDocument
)
from apps.datasource_knowledge_base.tasks import load_and_index_document
from apps.datasource_knowledge_base.utils import generate_document_uri

from apps.knowledge_base_store.models import (
    KnowledgeBaseIntegration
)

from apps.user_permissions.utils import (
    PermissionNames
)
from config import settings
from config.settings import MEDIA_URL

logger = logging.getLogger(__name__)


class KnowledgeBaseStoreView_IntegrateKnowledgeBase(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - INTEGRATE_KNOWLEDGE_BASE_FILES
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.INTEGRATE_KNOWLEDGE_BASE_FILES
        ):
            messages.error(
                self.request,
                "You do not have permission to integrate Knowledge Base files."
            )

            return redirect('knowledge_base_store:list')
        ##############################

        item_id = kwargs['pk']

        if not item_id:
            messages.error(
                self.request,
                "Knowledge Base Integration ID is missing."
            )

            logger.error("Knowledge Base Integration ID is missing.")

            return redirect('knowledge_base_store:list')

        integration_boilerplate: KnowledgeBaseIntegration = KnowledgeBaseIntegration.objects.get(
            id=item_id
        )

        if not integration_boilerplate:
            messages.error(
                self.request,
                "Knowledge Base Integration ID is invalid."
            )

            logger.error("Knowledge Base Integration ID is invalid.")

            return redirect('knowledge_base_store:list')

        connection_id = request.POST.get('connection_id')

        if not connection_id:
            messages.error(self.request, "Connection ID is missing.")

            logger.error("Connection ID is missing.")

            return redirect('knowledge_base_store:list')

        connection_storage: DocumentKnowledgeBaseConnection = (
            DocumentKnowledgeBaseConnection.objects.get(
                id=connection_id
            )
        )

        if not connection_storage:
            messages.error(self.request, "Connection ID is invalid.")

            logger.error("Connection ID is invalid.")

            return redirect('knowledge_base_store:list')

        object_url = integration_boilerplate.knowledge_base_download_url

        if not object_url:
            messages.error(
                self.request,
                "Knowledge Base Repository URL is missing."
            )

            logger.error("Knowledge Base Repository URL is missing.")

            return redirect('knowledge_base_store:list')

        try:

            response = requests.get(
                object_url
            )

            if response.status_code != 200:
                messages.error(self.request, "Knowledge Base Repository URL is invalid.")

                logger.error("Knowledge Base Repository URL is invalid.")

                return redirect('knowledge_base_store:list')

            logger.info("Knowledge Base Repository ZIP file downloaded successfully.")

            try:
                with zipfile.ZipFile(io.BytesIO(response.content)) as zf:

                    with TemporaryDirectory() as temp_dir:
                        zf.extractall(temp_dir)

                        logger.info("Extracted files to temporary directory.")

                        knowledge_base_documents = []

                        for root, _, files in os.walk(temp_dir):
                            for file in files:
                                file_path = os.path.join(root, file)
                                with open(file_path, 'rb') as f:
                                    content = f.read()
                                    file_like_object = io.BytesIO(content)

                                    knowledge_base_documents.append(
                                        {
                                            'file_name': file,
                                            'content': None,
                                            'file_like_object': file_like_object
                                        }
                                    )

                        logger.info("Successfully loaded knowledge base documents.")

            except zipfile.BadZipFile:
                messages.error(
                    self.request,
                    "The downloaded file is not a valid zip file."
                )

                logger.error("The downloaded file is not a valid zip file.")

                return redirect('knowledge_base_store:list')

            logger.info("Knowledge Base Documents loaded from resources successfully.")

            agent_base_dir = connection_storage.assistant.document_base_directory

            f_paths = []
            document_items = []

            for file in knowledge_base_documents:
                file_type = file["file_name"].split('.')[-1]
                structured_file_name = slugify(file["file_name"]) + f"_{str(uuid.uuid4()).replace('-', '')}"

                doc_uri = generate_document_uri(
                    agent_base_dir,
                    structured_file_name,
                    file_type
                )

                f_paths.append(doc_uri)

                bucket = settings.AWS_STORAGE_BUCKET_NAME
                bucket_path = f"{doc_uri.split(MEDIA_URL)[1]}"

                file["file_like_object"].seek(0)

                file_buffer = io.BytesIO(
                    file["file_like_object"].read()
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
                    knowledge_base=connection_storage,
                    document_type=file_type,
                    document_file_name=structured_file_name,
                    document_uri=doc_uri,
                    created_by_user=request.user
                )
                new_document.save()

                document_items.append(new_document)

                logger.info(f"Knowledge Base Document uploaded: {structured_file_name}")

        except Exception as e:
            messages.error(self.request, "Knowledge Base Repository URL is invalid.")

            logger.error(f"Knowledge Base Repository URL is invalid: {e.__str__()[0:1000]}")

            return redirect('knowledge_base_store:list')

        logger.info('Knowledge Base Documents uploaded to BimodLab storage successfully.')

        try:
            # Handle document indexing process
            success = load_and_index_document(
                items=document_items
            )

            if not success:
                logger.error('Error while indexing documents.')
                messages.error(request, 'Error while indexing documents.')

            logger.info(
                f"Knowledge Base Document Items integrated successfully."
            )

            messages.success(
                request,
                f"Knowledge Base Document Items integrated successfully."
            )

        except Exception as e:
            logger.error(f"Error while integrating Knowledge Base Documents.")

            messages.error(request, f"Error while integrating Knowledge Base Documents: {e}")

        logger.info('Knowledge Base Documents uploaded successfully.')

        return redirect('knowledge_base_store:list')
