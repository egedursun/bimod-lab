#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: repository_chunk_embedder.py
#  Last Modified: 2024-09-28 20:38:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:02:47
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

import datetime
import json

from apps.datasource_codebase.utils import RepositoryUploadStatusNames


def build_chunk_orm_structure(chunk: dict,
                              knowledge_base,
                              document_id: int,
                              document_uuid: str,
                              path: str,
                              chunk_index: int):
    from apps.datasource_codebase.models import CodeBaseRepositoryChunk
    from apps.datasource_codebase.models import CodeBaseRepository
    id, error = None, None
    try:
        chunk_knowledge_base = knowledge_base
        chunk_document = CodeBaseRepository.objects.filter(id=document_id).first()
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
        print(f"[repository_chunk_embedder.build_chunk_orm_structure] Chunk ORM object created.")
        id = chunk_orm_object.id
    except Exception as e:
        error = f"[repository_chunk_embedder.build_chunk_orm_structure] Error building the chunk ORM structure: {e}"
        print(error)
    return id, error


def build_chunk_weaviate_structure(chunk: dict, path: str,
                                   chunk_index: int,
                                   document_uuid: str):
    chunk_weaviate_object, error = None, None
    try:
        weaviate_chunk_document_file_name = str(path)
        weaviate_chunk_number = chunk_index
        weaviate_chunk_content = chunk["page_content"]
        weaviate_chunk_metadata = json.dumps(chunk["metadata"], default=str, sort_keys=True)
        weaviate_chunk_created_at = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        chunk_weaviate_object = {
            "repository_uuid": document_uuid,
            "chunk_repository_file_name": weaviate_chunk_document_file_name,
            "chunk_number": weaviate_chunk_number,
            "chunk_content": weaviate_chunk_content,
            "chunk_metadata": weaviate_chunk_metadata,
            "created_at": weaviate_chunk_created_at
        }
        print(f"[repository_chunk_embedder.build_chunk_weaviate_structure] Chunk Weaviate object created.")
    except Exception as e:
        error = f"[repository_chunk_embedder.build_chunk_weaviate_structure] Error building the chunk Weaviate structure: {e}"
        print(error)
    return chunk_weaviate_object, error

def embed_repository_chunk_sync(executor_params, chunk_id, chunk_weaviate_object: dict):
    from apps._services.codebase.codebase_decoder import CodeBaseDecoder
    from apps.datasource_codebase.models import (CodeRepositoryStorageConnection, CodeBaseRepositoryChunk)

    # Retrieve connection details
    connection_id = executor_params["connection_id"]
    connection_orm_object = CodeRepositoryStorageConnection.objects.get(id=connection_id)

    # Re-initialize the executor
    executor = CodeBaseDecoder.get(connection=connection_orm_object)
    c = executor.connect_c()
    if not c:
        print(f"[repository_chunk_embedder.embed_repository_chunk_sync]: Error while connecting to Weaviate")
    print(f"[repository_chunk_embedder.embed_repository_chunk_sync]: Connected to Weaviate successfully.")

    error = None
    try:
        # Save the object to Weaviate
        chunk_class_name = f"{executor.connection_object.class_name}Chunks"
        collection = c.collections.get(chunk_class_name)
        uuid = collection.data.insert(properties=chunk_weaviate_object)
        print(f"[repository_chunk_embedder.embed_repository_chunk_sync]: Chunk inserted successfully.")
        if not uuid:
            error = "Error inserting the chunk into Weaviate"

        # Save the object to the ORM
        chunk_orm_object: CodeBaseRepositoryChunk = CodeBaseRepositoryChunk.objects.filter(id=chunk_id).first()
        chunk_orm_object.chunk_uuid = str(uuid)
        chunk_orm_object.save()
        print(f"[repository_chunk_embedder.embed_repository_chunk_sync]: Chunk saved to the ORM successfully.")

        # add the chunk to the document chunks
        document = chunk_orm_object.repository
        document.repository_chunks.add(chunk_orm_object)
        document.save()
        print(f"[repository_chunk_embedder.embed_repository_chunk_sync]: Chunk saved to the ORM successfully.")

    except Exception as e:
        error = f"[repository_chunk_embedder.embed_repository_chunk_sync] Error embedding the chunk: {e}"
        print(error)
    print(f"[repository_chunk_embedder.embed_repository_chunk_sync]: Exiting the function.")
    return error


def embed_repository_chunks_helper(executor_params, chunks: list, path: str, document_id: int,
                                 document_uuid: str):
    from apps.datasource_codebase.models import CodeRepositoryStorageConnection
    from apps.datasource_codebase.tasks import add_repository_upload_log
    errors = []
    connection_id = executor_params["connection_id"]
    connection_orm_object = CodeRepositoryStorageConnection.objects.get(id=connection_id)
    print(f"[repository_chunk_embedder.embed_repository_chunks_helper] Embedding chunks...")
    try:
        for i, chunk in enumerate(chunks):
            chunk_id, error = build_chunk_orm_structure(
                knowledge_base=connection_orm_object,
                chunk=chunk,
                path=path,
                chunk_index=i,
                document_id=document_id,
                document_uuid=document_uuid
            )
            if error:
                errors.append(error)
                continue

            document_weaviate_object, error = build_chunk_weaviate_structure(
                chunk=chunk,
                path=path,
                chunk_index=i,
                document_uuid=document_uuid
            )
            if error:
                errors.append(error)
                continue

            print(f"Embedding chunk: {i}")
            error = embed_repository_chunk_sync(
                executor_params=executor_params,
                chunk_id=chunk_id,
                chunk_weaviate_object=document_weaviate_object
            )
            if error:
                errors.append(error)
                continue
        add_repository_upload_log(document_full_uri=path, log_name=RepositoryUploadStatusNames.EMBEDDED_CHUNKS)
        add_repository_upload_log(document_full_uri=path, log_name=RepositoryUploadStatusNames.SAVED_CHUNKS)
    except Exception as e:
        errors.append(f"[repository_chunk_embedder.embed_repository_chunks_helper] Error embedding the chunks: {e}")
    print(f"[repository_chunk_embedder.embed_repository_chunks_helper] Exiting the function.")
    return errors
