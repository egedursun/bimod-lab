#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: repository_embedder.py
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

import json
import logging

from apps.datasource_codebase.utils import RepositoryUploadStatusNames


logger = logging.getLogger(__name__)


def build_repository_orm_structure(document: dict, knowledge_base, path: str):
    from apps.datasource_codebase.models import CodeBaseRepository
    _id, error = None, None
    try:
        doc_knowledge_base = knowledge_base
        doc_file_name = path.split("/")[-1]
        doc_document_uri = path
        doc_description = ""
        doc_document_content_temporary = ""
        doc_metadata = document["metadata"]
        document_orm_object = CodeBaseRepository.objects.create(
            knowledge_base=doc_knowledge_base,
            repository_name=doc_file_name,
            repository_description=doc_description,
            repository_metadata=doc_metadata,
            repository_uri=doc_document_uri,
            repository_content_temporary=doc_document_content_temporary,
        )
        document_orm_object.save()
        _id = document_orm_object.id
        logger.info(f"[repository_embedder.build_repository_orm_structure] Built the repository ORM structure")
    except Exception as e:
        logger.error(f"[repository_embedder.build_repository_orm_structure] Error building the repository ORM structure: {e}")
        error = f"[repository_embedder.build_repository_orm_structure] Error building the repository ORM structure: {e}"
    return _id, error


def build_repository_weaviate_structure(document: dict, path: str,
                                        number_of_chunks: int):
    document_weaviate_object, error = None, None
    try:
        weaviate_document_file_name = path.split("/")[-1]
        weaviate_document_description = ""
        weaviate_document_metadata = json.dumps(document["metadata"], default=str, sort_keys=True)
        weaviate_document_number_of_chunks = number_of_chunks
        weaviate_document_created_at = ""
        document_weaviate_object = {
            "repository_file_name": weaviate_document_file_name,
            "repository_description": weaviate_document_description, "repository_metadata": weaviate_document_metadata,
            "number_of_chunks": weaviate_document_number_of_chunks, "created_at": weaviate_document_created_at}
        logger.info(f"[repository_embedder.build_repository_weaviate_structure] Built the repository Weaviate structure")
    except Exception as e:
        logger.error(f"[repository_embedder.build_repository_weaviate_structure] Error building the repository Weaviate structure: {e}")
        error = (f"[repository_embedder.build_repository_weaviate_structure] Error building the "
                 f"repository Weaviate structure: {e}")
    return document_weaviate_object, error


def embed_repository_sync(executor_params, document_id, document_weaviate_object: dict, path: str):
    from apps.core.codebase.codebase_decoder import CodeBaseDecoder
    from apps.datasource_codebase.models import (CodeRepositoryStorageConnection, CodeBaseRepository)
    from apps.datasource_codebase.tasks import add_repository_upload_log
    conn_id = executor_params["connection_id"]
    conn_orm_obj = CodeRepositoryStorageConnection.objects.get(id=conn_id)
    xc = CodeBaseDecoder.get(connection=conn_orm_obj)
    c = xc.connect_c()
    error, uuid = None, None
    try:
        collection = c.collections.get(xc.connection_object.class_name)
        uuid = collection.data.insert(properties=document_weaviate_object)
        if not uuid:
            error = "[document_embedder.embed_document_sync] Error inserting the document into Weaviate"
            logger.error(error)
        add_repository_upload_log(document_full_uri=path, log_name=RepositoryUploadStatusNames.EMBEDDED_DOCUMENT)
        document_orm_object = CodeBaseRepository.objects.get(id=document_id)
        document_orm_object.knowledge_base_uuid = str(uuid)
        try:
            document_orm_object.save()
            logger.info("[repository_embedder.embed_repository_sync] Saved the repository ORM object into DB")
        except Exception as e:
            logger.error(f"[repository_embedder.embed_repository_sync] Error saving the repository ORM object into DB: {e}")
            error = f"[repository_embedder.embed_repository_sync] Error saving the repository ORM object into DB: {e}"
        add_repository_upload_log(document_full_uri=path, log_name=RepositoryUploadStatusNames.SAVED_DOCUMENT)
    except Exception as e:
        logger.error(f"[repository_embedder.embed_repository_sync] Error embedding the repository: {e}")
        error = f"[repository_embedder.embed_repository_sync] Error embedding the repository: {e}"
    return uuid, error


def embed_repository_helper(executor_params: dict, document: dict, path: str, number_of_chunks: int):
    from apps.datasource_codebase.models import CodeRepositoryStorageConnection
    document_id, document_uuid = None, None
    conn_id = executor_params["connection_id"]
    conn_orm_obj = CodeRepositoryStorageConnection.objects.get(id=conn_id)
    try:
        document_id, error = build_repository_orm_structure(
            knowledge_base=conn_orm_obj, document=document, path=path)
        if error:
            logger.error(error)
            return document_id, document_uuid, error

        document_weaviate_object, error = build_repository_weaviate_structure(
            document=document, path=path, number_of_chunks=number_of_chunks)
        if error:
            logger.error(error)
            return document_id, document_uuid, error

        document_uuid, error = embed_repository_sync(
            executor_params=executor_params, document_id=document_id,
            document_weaviate_object=document_weaviate_object, path=path)
        if error:
            logger.error(error)
            return document_id, document_uuid, error
    except Exception as e:
        logger.error(f"[repository_embedder.embed_repository_helper] Error embedding the repository: {e}")
        return f"[repository_embedder.embed_repository_helper] Error embedding the repository: {e}"
    logger.info("[repository_embedder.embed_repository_helper] Successfully embedded the repository")
    return document_id, document_uuid, error
