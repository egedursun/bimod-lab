#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#

import json

from apps.datasource_codebase.utils import RepositoryUploadStatusNames


def build_repository_orm_structure(document: dict, knowledge_base, path: str):
    from apps.datasource_codebase.models import CodeBaseRepository
    id, error = None, None
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
        id = document_orm_object.id
        print(f"[repository_embedder.build_repository_orm_structure] Repository ORM object created successfully.")
    except Exception as e:
        error = f"[repository_embedder.build_repository_orm_structure] Error building the repository ORM structure: {e}"
    return id, error


def build_repository_weaviate_structure(document: dict, path: str,
                                        number_of_chunks: int):
    document_weaviate_object, error = None, None
    try:
        weav_document_file_name = path.split("/")[-1]
        weav_document_description = ""
        weav_document_metadata = json.dumps(document["metadata"], default=str, sort_keys=True)
        weave_document_number_of_chunks = number_of_chunks
        weave_document_created_at = ""  # empty for now

        document_weaviate_object = {
            "repository_file_name": weav_document_file_name,
            "repository_description": weav_document_description,
            "repository_metadata": weav_document_metadata,
            "number_of_chunks": weave_document_number_of_chunks,
            "created_at": weave_document_created_at
        }
        print(
            f"[repository_embedder.build_repository_weaviate_structure] Repository Weaviate object created successfully.")
    except Exception as e:
        error = f"[repository_embedder.build_repository_weaviate_structure] Error building the repository Weaviate structure: {e}"
    return document_weaviate_object, error


def embed_repository_sync(executor_params, document_id, document_weaviate_object: dict, path: str):
    from apps._services.codebase.codebase_decoder import CodeBaseDecoder
    from apps.datasource_codebase.models import (CodeRepositoryStorageConnection, CodeBaseRepository)
    from apps.datasource_codebase.tasks import add_repository_upload_log
    connection_id = executor_params["connection_id"]
    connection_orm_object = CodeRepositoryStorageConnection.objects.get(id=connection_id)
    executor = CodeBaseDecoder.get(connection=connection_orm_object)
    c = executor.connect_c()
    if not c:
        print(f"[repository_embedder.embed_repository_sync] Error while connecting to Weaviate")
    print(f"[repository_embedder.embed_repository_sync] Repository Weaviate object created.")

    error, uuid = None, None
    try:
        # Save the object to Weaviate
        collection = c.collections.get(executor.connection_object.class_name)
        uuid = collection.data.insert(properties=document_weaviate_object)
        if not uuid:
            error = "[document_embedder.embed_document_sync] Error inserting the document into Weaviate"
        add_repository_upload_log(document_full_uri=path, log_name=RepositoryUploadStatusNames.EMBEDDED_DOCUMENT)

        document_orm_object = CodeBaseRepository.objects.get(id=document_id)
        document_orm_object.knowledge_base_uuid = str(uuid)
        print(f"[repository_embedder.embed_repository_sync] Repository ORM object created.")
        try:
            document_orm_object.save()
        except Exception as e:
            error = f"[repository_embedder.embed_repository_sync] Error saving the repository ORM object into DB: {e}"
            print(error)
        add_repository_upload_log(document_full_uri=path, log_name=RepositoryUploadStatusNames.SAVED_DOCUMENT)
    except Exception as e:
        error = f"[repository_embedder.embed_repository_sync] Error embedding the repository: {e}"
    print(f"[repository_embedder.embed_repository_sync] Repository embedded successfully.")
    return uuid, error


def embed_repository_helper(executor_params: dict, document: dict, path: str, number_of_chunks: int):
    from apps.datasource_codebase.models import CodeRepositoryStorageConnection
    document_id, document_uuid = None, None
    connection_id = executor_params["connection_id"]
    connection_orm_object = CodeRepositoryStorageConnection.objects.get(id=connection_id)

    try:
        document_id, error = build_repository_orm_structure(
            knowledge_base=connection_orm_object,
            document=document,
            path=path
        )
        if error:
            print(
                f"[repository_embedder.embed_repository_helper] Error building the repository ORM structure: {error}")
            return document_id, document_uuid, error
        print(f"[repository_embedder.embed_repository_helper] Repository ORM object created successfully.")

        document_weaviate_object, error = build_repository_weaviate_structure(
            document=document,
            path=path,
            number_of_chunks=number_of_chunks
        )
        if error:
            print(
                f"[repository_embedder.embed_repository_helper] Error building the repository Weaviate structure: {error}")
            return document_id, document_uuid, error
        print(f"[repository_embedder.embed_repository_helper] Repository Weaviate object created successfully.")

        document_uuid, error = embed_repository_sync(
            executor_params=executor_params,
            document_id=document_id,
            document_weaviate_object=document_weaviate_object,
            path=path
        )
        if error:
            print(
                f"[repository_embedder.embed_repository_helper] Error embedding the repository and saving the ORM object: {error}")
            return document_id, document_uuid, error
    except Exception as e:
        return f"[repository_embedder.embed_repository_helper] Error embedding the repository: {e}"
    print(f"[repository_embedder.embed_repository_helper] Repository embedded successfully.")
    return document_id, document_uuid, error
