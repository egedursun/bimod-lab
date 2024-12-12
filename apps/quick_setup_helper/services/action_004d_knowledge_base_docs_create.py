#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: action_004d_knowledge_base_docs_create.py
#  Last Modified: 2024-12-11 23:19:39
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-11 23:19:40
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
from slugify import slugify

from apps.assistants.models import (
    Assistant
)

from apps.datasource_knowledge_base.models import (
    KnowledgeBaseDocument
)

from apps.datasource_knowledge_base.tasks import (
    load_and_index_document
)

from apps.datasource_knowledge_base.utils import (
    generate_document_uri
)

from config import settings

from config.settings import MEDIA_URL

logger = logging.getLogger(__name__)


def action_004d_knowledge_base_docs_create(
    metadata__user,
    metadata__assistants,
    metadata__documents,
):
    try:

        for assistant in metadata__assistants:
            assistant: Assistant

            try:

                vector_store = assistant.documentknowledgebaseconnection_set.first()

                if vector_store and metadata__documents and len(metadata__documents) > 0:

                    agent_base_dir = vector_store.assistant.document_base_directory
                    f_paths = []
                    document_items = []

                    for file in metadata__documents:
                        file_type = file.name.split('.')[-1]
                        structured_file_name = slugify(file.name) + f"_{str(uuid.uuid4).replace('-', '')}"

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
                            created_by_user=metadata__user
                        )

                        new_document.save()

                        document_items.append(new_document)

                        logger.info(f"Document has been uploaded: {structured_file_name}")

                    # Handle document indexing process
                    success = load_and_index_document(
                        items=document_items
                    )

                    if not success:
                        logger.error('Error while indexing documents.')
                        continue

            except Exception as e:
                logger.error(f"Error while creating Knowledge Base Documents for assistant {assistant.name}: {e}")

                return False

    except Exception as e:
        logger.error(f"Error while creating Knowledge Base Documents: {e}")

        return False

    logger.info("action__004d_knowledge_base_docs_create completed successfully.")

    return True
