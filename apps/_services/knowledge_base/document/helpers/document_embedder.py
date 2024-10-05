#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: document_embedder.py
#  Last Modified: 2024-09-28 22:17:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:35
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: document_embedder.py
#  Last Modified: 2024-09-28 20:38:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:05:43
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

import json

from apps.datasource_knowledge_base.utils import DocumentUploadStatusNames


def build_document_orm_structure(document: dict, knowledge_base, path: str):
    from apps.datasource_knowledge_base.models import KnowledgeBaseDocument
    id, error = None, None
    try:
        doc_knowledge_base = knowledge_base
        doc_file_type = path.split(".")[-1]
        doc_file_name = path.split("/")[-1]
        doc_document_uri = path
        doc_description = ""  # empty for now
        doc_document_content_temporary = ""  # empty for now
        doc_metadata = document["metadata"]

        document_orm_object = KnowledgeBaseDocument.objects.create(
            knowledge_base=doc_knowledge_base,
            document_type=doc_file_type,
            document_file_name=doc_file_name,
            document_description=doc_description,
            document_metadata=doc_metadata,
            document_uri=doc_document_uri,
            document_content_temporary=doc_document_content_temporary,
        )
        document_orm_object.save()
        id = document_orm_object.id
        print(f"[document_embedder.build_document_orm_structure] Document ORM object created successfully.")
    except Exception as e:
        error = f"[document_embedder.build_document_orm_structure] Error building the document ORM structure: {e}"
    return id, error


def build_memory_orm_structure(memory_name: str, knowledge_base):
    from apps.datasource_knowledge_base.models import ContextHistoryMemory
    id, error = None, None
    try:
        memory_orm_object = ContextHistoryMemory.objects.create(
            context_history_base=knowledge_base,
            memory_name=memory_name
        )
        memory_orm_object.save()
        id = memory_orm_object.id
        print(f"[document_embedder.build_memory_orm_structure] Memory ORM object created successfully.")
    except Exception as e:
        error = f"[document_embedder.build_memory_orm_structure] Error building the memory ORM structure: {e}"
    return id, error


def build_document_weaviate_structure(document: dict, path: str,
                                      number_of_chunks: int):
    document_weaviate_object, error = None, None
    try:
        weav_document_file_name = path.split("/")[-1]
        weav_document_description = ""  # empty for now
        weav_document_type = path.split(".")[-1]
        weav_document_metadata = json.dumps(document["metadata"], default=str, sort_keys=True)
        weave_document_number_of_chunks = number_of_chunks
        weave_document_created_at = ""  # empty for now

        document_weaviate_object = {
            "document_file_name": weav_document_file_name,
            "document_description": weav_document_description,
            "document_type": weav_document_type,
            "document_metadata": weav_document_metadata,
            "number_of_chunks": weave_document_number_of_chunks,
            "created_at": weave_document_created_at
        }
        print(f"[document_embedder.build_document_weaviate_structure] Document Weaviate object created successfully.")
    except Exception as e:
        error = f"[document_embedder.build_document_weaviate_structure] Error building the document Weaviate structure: {e}"
    return document_weaviate_object, error


def build_memory_weaviate_structure(memory_name: str, number_of_chunks: int):
    memory_weaviate_object, error = None, None
    try:
        weave_memory_name = memory_name
        weave_memory_created_at = ""  # empty for now

        memory_weaviate_object = {
            "memory_name": weave_memory_name,
            "created_at": weave_memory_created_at,
            "number_of_chunks": number_of_chunks
        }
        print(f"[document_embedder.build_memory_weaviate_structure] Memory Weaviate object created successfully.")
    except Exception as e:
        error = f"[document_embedder.build_memory_weaviate_structure] Error building the memory Weaviate structure: {e}"
    return memory_weaviate_object, error


def embed_document_sync(executor_params, document_id, document_weaviate_object: dict, path: str):
    from apps._services.knowledge_base.document.knowledge_base_decoder import KnowledgeBaseSystemDecoder
    from apps.datasource_knowledge_base.models import (DocumentKnowledgeBaseConnection, KnowledgeBaseDocument)
    from apps.datasource_knowledge_base.tasks import add_document_upload_log
    connection_id = executor_params["connection_id"]
    connection_orm_object = DocumentKnowledgeBaseConnection.objects.get(id=connection_id)
    executor = KnowledgeBaseSystemDecoder.get(connection=connection_orm_object)
    c = executor.connect_c()
    if not c:
        print(f"[document_embedder.embed_document_sync] Error while connecting to Weaviate")
    print(f"[document_embedder.embed_document_sync] Document Weaviate object created.")

    error, uuid = None, None
    try:
        # Save the object to Weaviate
        collection = c.collections.get(executor.connection_object.class_name)
        uuid = collection.data.insert(properties=document_weaviate_object)
        if not uuid:
            error = "[document_embedder.embed_document_sync] Error inserting the document into Weaviate"
        add_document_upload_log(document_full_uri=path, log_name=DocumentUploadStatusNames.EMBEDDED_DOCUMENT)

        document_orm_object = KnowledgeBaseDocument.objects.get(id=document_id)
        document_orm_object.knowledge_base_uuid = str(uuid)
        print(f"[document_embedder.embed_document_sync] Document ORM object created.")
        try:
            document_orm_object.save()
        except Exception as e:
            error = f"[document_embedder.embed_document_sync] Error saving the document ORM object into DB: {e}"
            print(error)
        add_document_upload_log(document_full_uri=path, log_name=DocumentUploadStatusNames.SAVED_DOCUMENT)
    except Exception as e:
        error = f"[document_embedder.embed_document_sync] Error embedding the document: {e}"
    print(f"[document_embedder.embed_document_sync] Document embedded successfully.")
    return uuid, error


def embed_memory_sync(executor_params, memory_id, memory_weaviate_object: dict):
    from apps.datasource_knowledge_base.models import (ContextHistoryKnowledgeBaseConnection, ContextHistoryMemory)
    from apps._services.knowledge_base.memory.memory_executor import MemoryExecutor
    connection_id = executor_params["connection_id"]
    connection_orm_object = ContextHistoryKnowledgeBaseConnection.objects.get(id=connection_id)
    executor = MemoryExecutor(connection=connection_orm_object)
    c = executor.connect_c()
    if not c:
        print(f"[document_embedder.embed_memory_sync]: Error while connecting to Weaviate")
    error, uuid = None, None
    try:
        # Save the object to Weaviate
        collection = c.collections.get(executor.connection_object.class_name)
        uuid = collection.data.insert(properties=memory_weaviate_object)
        if not uuid:
            error = "[document_embedder.embed_memory_sync] Error inserting the memory item into Weaviate"
        print(f"[document_embedder.embed_memory_sync] Memory Weaviate object created.")

        memory_orm_object = ContextHistoryMemory.objects.get(id=memory_id)
        memory_orm_object.knowledge_base_memory_uuid = str(uuid)
        print(f"[document_embedder.embed_memory_sync] Memory ORM object created.")
        try:
            memory_orm_object.save()
        except Exception as e:
            error = f"[document_embedder.embed_memory_sync] Error saving the memory ORM object into DB: {e}"
            print(error)
    except Exception as e:
        error = f"[document_embedder.embed_memory_sync] Error embedding the memory: {e}"
    print(f"[document_embedder.embed_memory_sync] Memory embedded successfully.")
    return uuid, error


def embed_document_helper(executor_params: dict, document: dict, path: str, number_of_chunks: int):
    from apps.datasource_knowledge_base.models import DocumentKnowledgeBaseConnection
    document_id, document_uuid = None, None
    connection_id = executor_params["connection_id"]
    connection_orm_object = DocumentKnowledgeBaseConnection.objects.get(id=connection_id)

    try:
        document_id, error = build_document_orm_structure(
            knowledge_base=connection_orm_object,
            document=document,
            path=path
        )
        if error:
            print(f"[document_embedder.embed_document_helper] Error building the document ORM structure: {error}")
            return document_id, document_uuid, error
        print(f"[document_embedder.embed_document_helper] Document ORM object created successfully.")

        document_weaviate_object, error = build_document_weaviate_structure(
            document=document,
            path=path,
            number_of_chunks=number_of_chunks
        )
        if error:
            print(f"[document_embedder.embed_document_helper] Error building the document Weaviate structure: {error}")
            return document_id, document_uuid, error
        print(f"[document_embedder.embed_document_helper] Document Weaviate object created successfully.")

        document_uuid, error = embed_document_sync(
            executor_params=executor_params,
            document_id=document_id,
            document_weaviate_object=document_weaviate_object,
            path=path
        )
        if error:
            print(
                f"[document_embedder.embed_document_helper] Error embedding the document and saving the ORM object: {error}")
            return document_id, document_uuid, error
    except Exception as e:
        return f"[document_embedder.embed_document_helper] Error embedding the document: {e}"
    print(f"[document_embedder.embed_document_helper] Document embedded successfully.")
    return document_id, document_uuid, error


def embed_memory_helper(executor_params: dict, number_of_chunks: int):
    from apps.datasource_knowledge_base.models import ContextHistoryKnowledgeBaseConnection
    memory_id, memory_uuid = None, None
    connection_id = executor_params["connection_id"]
    connection_orm_object = ContextHistoryKnowledgeBaseConnection.objects.get(id=connection_id)
    from apps.datasource_knowledge_base.utils import generate_random_alphanumeric
    memory_name = generate_random_alphanumeric(numeric_component=False)
    print(f"[document_embedder.embed_memory_helper] Memory name: {memory_name}")

    try:
        memory_id, error = build_memory_orm_structure(
            knowledge_base=connection_orm_object,
            memory_name=memory_name
        )
        if error:
            print(f"[document_embedder.embed_memory_helper] Error building the memory ORM structure: {error}")
            return memory_id, memory_uuid, error
        print(f"[document_embedder.embed_memory_helper] Memory ORM object created successfully.")

        memory_weaviate_object, error = build_memory_weaviate_structure(
            memory_name=memory_name,
            number_of_chunks=number_of_chunks
        )
        if error:
            print(f"[document_embedder.embed_memory_helper] Error building the memory Weaviate structure: {error}")
            return memory_id, memory_uuid, error
        print(f"[document_embedder.embed_memory_helper] Memory Weaviate object created successfully.")

        memory_uuid, error = embed_memory_sync(
            executor_params=executor_params,
            memory_id=memory_id,
            memory_weaviate_object=memory_weaviate_object
        )
        if error:
            print(
                f"[document_embedder.embed_memory_helper] Error embedding the memory and saving the ORM object: {error}")
            return memory_id, memory_uuid, error

    except Exception as e:
        return f"[document_embedder.embed_memory_helper] Error embedding the memory: {e}"
    print(f"[document_embedder.embed_memory_helper] Memory embedded successfully.")
    return memory_id, memory_uuid, error
