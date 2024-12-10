#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: repository_chunk_embedder.py
#  Last Modified: 2024-10-05 02:20:19
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:36
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import datetime
import json
import logging

from apps.datasource_codebase.utils import (
    RepositoryUploadStatusNames
)

logger = logging.getLogger(__name__)


def build_chunk_orm_structure(
    chunk: dict,
    knowledge_base,
    document_id: int,
    document_uuid: str,
    path: str,
    chunk_index: int
):
    from apps.datasource_codebase.models import (
        CodeBaseRepositoryChunk
    )

    from apps.datasource_codebase.models import (
        CodeBaseRepository
    )

    _id, error = None, None
    try:
        chunk_knowledge_base = knowledge_base

        chunk_document = CodeBaseRepository.objects.filter(
            id=document_id
        ).first()

        chunk_document_uuid = document_uuid
        chunk_number = chunk_index
        chunk_content = chunk["page_content"]
        chunk_metadata = chunk["metadata"]
        chunk_document_uri = path

        chunk_orm_object = CodeBaseRepositoryChunk.objects.create(
            knowledge_base=chunk_knowledge_base,
            chunk_number=chunk_number,
            chunk_content=chunk_content,
            chunk_metadata=chunk_metadata,
            chunk_repository_uri=chunk_document_uri,
            repository=chunk_document,
            repository_uuid=chunk_document_uuid
        )

        _id = chunk_orm_object.id
        logger.info(f"[repository_chunk_embedder.build_chunk_orm_structure] Built the chunk ORM structure")

    except Exception as e:
        logger.error(
            f"[repository_chunk_embedder.build_chunk_orm_structure] Error building the chunk ORM structure: {e}")

        error = f"[repository_chunk_embedder.build_chunk_orm_structure] Error building the chunk ORM structure: {e}"

    return _id, error


def build_chunk_weaviate_structure(
    chunk: dict,
    path: str,
    chunk_index: int,
    document_uuid: str
):
    chunk_weaviate_object, error = None, None

    try:
        weaviate_chunk_document_file_name = str(path)
        weaviate_chunk_number = chunk_index
        weaviate_chunk_content = chunk["page_content"]

        weaviate_chunk_metadata = json.dumps(
            chunk["metadata"],
            default=str,
            sort_keys=True
        )

        weaviate_chunk_created_at = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        chunk_weaviate_object = {
            "repository_uuid": document_uuid,
            "chunk_repository_file_name": weaviate_chunk_document_file_name,
            "chunk_number": weaviate_chunk_number,
            "chunk_content": weaviate_chunk_content,
            "chunk_metadata": weaviate_chunk_metadata,
            "created_at": weaviate_chunk_created_at
        }

        logger.info(f"[repository_chunk_embedder.build_chunk_weaviate_structure] Built the chunk Weaviate structure")

    except Exception as e:
        logger.error(
            f"[repository_chunk_embedder.build_chunk_weaviate_structure] Error building the chunk Weaviate structure: {e}")

        error = (f"[repository_chunk_embedder.build_chunk_weaviate_structure] Error building "
                 f"the chunk Weaviate structure: {e}")

    return chunk_weaviate_object, error


def embed_repository_chunk_sync(
    executor_params,
    chunk_id,
    chunk_weaviate_object: dict
):
    from apps.core.codebase.codebase_decoder import (
        CodeBaseDecoder
    )

    from apps.datasource_codebase.models import (
        CodeRepositoryStorageConnection,
        CodeBaseRepositoryChunk
    )

    conn_id = executor_params["connection_id"]

    conn_orm_obj = CodeRepositoryStorageConnection.objects.get(
        id=conn_id
    )

    xc = CodeBaseDecoder.get(
        connection=conn_orm_obj
    )

    c = xc.connect_c()
    error = None

    try:
        chunk_class_name = f"{xc.connection_object.class_name}Chunks"
        collection = c.collections.get(chunk_class_name)

        uuid = collection.data.insert(
            properties=chunk_weaviate_object
        )

        if not uuid:
            error = "Error inserting the chunk into Weaviate"
            logger.error(f"[repository_chunk_embedder.embed_repository_chunk_sync] {error}")

        chunk_orm_object: CodeBaseRepositoryChunk = CodeBaseRepositoryChunk.objects.filter(
            id=chunk_id
        ).first()

        chunk_orm_object.chunk_uuid = str(uuid)
        chunk_orm_object.save()

        document = chunk_orm_object.repository
        document.repository_chunks.add(chunk_orm_object)
        document.save()

        logger.info(f"[repository_chunk_embedder.embed_repository_chunk_sync] Embedded the chunk")

    except Exception as e:
        logger.error(f"[repository_chunk_embedder.embed_repository_chunk_sync] Error embedding the chunk: {e}")

        error = f"[repository_chunk_embedder.embed_repository_chunk_sync] Error embedding the chunk: {e}"

    return error


def embed_repository_chunks_helper(
    executor_params,
    chunks: list,
    path: str,
    document_id: int,
    document_uuid: str
):
    from apps.datasource_codebase.models import (
        CodeRepositoryStorageConnection
    )

    from apps.datasource_codebase.tasks import (
        add_repository_upload_log
    )

    errors = []
    conn_id = executor_params["connection_id"]

    conn_orm_obj = CodeRepositoryStorageConnection.objects.get(
        id=conn_id
    )

    try:

        for i, chunk in enumerate(chunks):
            chunk_id, error = build_chunk_orm_structure(
                knowledge_base=conn_orm_obj,
                chunk=chunk,
                path=path,
                chunk_index=i,
                document_id=document_id,
                document_uuid=document_uuid
            )

            if error:
                errors.append(error)
                logger.error(error)
                continue

            document_weaviate_object, error = build_chunk_weaviate_structure(
                chunk=chunk,
                path=path,
                chunk_index=i,
                document_uuid=document_uuid
            )

            if error:
                errors.append(error)
                logger.error(error)
                continue

            error = embed_repository_chunk_sync(
                executor_params=executor_params,
                chunk_id=chunk_id,
                chunk_weaviate_object=document_weaviate_object
            )

        if error:
            errors.append(error)
            logger.error(error)
            continue

        add_repository_upload_log(
            document_full_uri=path,
            log_name=RepositoryUploadStatusNames.EMBEDDED_CHUNKS
        )

        add_repository_upload_log(
            document_full_uri=path,
            log_name=RepositoryUploadStatusNames.SAVED_CHUNKS
        )

    except Exception as e:
        logger.error(f"[repository_chunk_embedder.embed_repository_chunks_helper] Error embedding the chunks: {e}")

        errors.append(f"[repository_chunk_embedder.embed_repository_chunks_helper] Error embedding the chunks: {e}")

    return errors
