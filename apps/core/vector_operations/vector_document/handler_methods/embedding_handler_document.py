#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: document_embedder.py
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
#
#

import json
import logging

from apps.datasource_knowledge_base.utils import VectorStoreDocProcessingStatusNames


logger = logging.getLogger(__name__)


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
        logger.info(f"[document_embedder.build_document_orm_structure] Document ORM object created successfully.")
    except Exception as e:
        logger.error(f"[document_embedder.build_document_orm_structure] Error building the document ORM structure: {e}")
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
        logger.info(f"[document_embedder.build_memory_orm_structure] Memory ORM object created successfully.")
    except Exception as e:
        logger.error(f"[document_embedder.build_memory_orm_structure] Error building the memory ORM structure: {e}")
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
        logger.info(f"[document_embedder.build_document_weaviate_structure] Document Weaviate object created successfully.")
    except Exception as e:
        logger.error(f"[document_embedder.build_document_weaviate_structure] Error building the document Weaviate structure: {e}")
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
        logger.info(f"[document_embedder.build_memory_weaviate_structure] Memory Weaviate object created successfully.")
    except Exception as e:
        logger.error(f"[document_embedder.build_memory_weaviate_structure] Error building the memory Weaviate structure: {e}")
        error = f"[document_embedder.build_memory_weaviate_structure] Error building the memory Weaviate structure: {e}"
    return memory_weaviate_object, error


def embed_document_sync(executor_params, document_id, document_weaviate_object: dict, path: str):
    from apps.core.vector_operations.vector_document.vector_store_decoder import KnowledgeBaseSystemDecoder
    from apps.datasource_knowledge_base.models import (DocumentKnowledgeBaseConnection, KnowledgeBaseDocument)
    from apps.datasource_knowledge_base.tasks import add_vector_store_doc_loaded_log
    connection_id = executor_params["connection_id"]
    connection_orm_object = DocumentKnowledgeBaseConnection.objects.get(id=connection_id)
    executor = KnowledgeBaseSystemDecoder.get(connection=connection_orm_object)
    c = executor.connect_c()
    if not c:
        logger.error(f"[document_embedder.embed_document_sync] Error while connecting to Weaviate")
    logger.info(f"[document_embedder.embed_document_sync] Document ORM object created.")

    error, uuid = None, None
    try:
        # Save the object to Weaviate
        collection = c.collections.get(executor.connection_object.class_name)
        uuid = collection.data.insert(properties=document_weaviate_object)
        if not uuid:
            logger.error("[document_embedder.embed_document_sync] Error inserting the document into Weaviate")
            error = "[document_embedder.embed_document_sync] Error inserting the document into Weaviate"
        add_vector_store_doc_loaded_log(document_full_uri=path, log_name=VectorStoreDocProcessingStatusNames.EMBEDDED_DOCUMENT)

        document_orm_object = KnowledgeBaseDocument.objects.get(id=document_id)
        document_orm_object.knowledge_base_uuid = str(uuid)
        try:
            document_orm_object.save()
        except Exception as e:
            logger.error(f"[document_embedder.embed_document_sync] Error saving the document ORM object into DB: {e}")
            error = f"[document_embedder.embed_document_sync] Error saving the document ORM object into DB: {e}"
        add_vector_store_doc_loaded_log(document_full_uri=path, log_name=VectorStoreDocProcessingStatusNames.SAVED_DOCUMENT)
    except Exception as e:
        logger.error(f"[document_embedder.embed_document_sync] Error embedding the document: {e}")
        error = f"[document_embedder.embed_document_sync] Error embedding the document: {e}"
    logger.info(f"[document_embedder.embed_document_sync] Document embedded successfully.")
    return uuid, error


def embed_memory_sync(executor_params, memory_id, memory_weaviate_object: dict):
    from apps.datasource_knowledge_base.models import (ContextHistoryKnowledgeBaseConnection, ContextHistoryMemory)
    from apps.core.vector_operations.intra_context_memory.memory_executor import IntraContextMemoryExecutor
    connection_id = executor_params["connection_id"]
    connection_orm_object = ContextHistoryKnowledgeBaseConnection.objects.get(id=connection_id)
    executor = IntraContextMemoryExecutor(connection=connection_orm_object)
    c = executor.connect_c()
    if not c:
        logger.error(f"[document_embedder.embed_memory_sync] Error while connecting to Weaviate")
    error, uuid = None, None
    try:
        # Save the object to Weaviate
        collection = c.collections.get(executor.connection_object.class_name)
        uuid = collection.data.insert(properties=memory_weaviate_object)
        if not uuid:
            logger.error("[document_embedder.embed_memory_sync] Error inserting the memory item into Weaviate")
            error = "[document_embedder.embed_memory_sync] Error inserting the memory item into Weaviate"
        logger.info(f"[document_embedder.embed_memory_sync] Memory ORM object created.")

        memory_orm_object = ContextHistoryMemory.objects.get(id=memory_id)
        memory_orm_object.knowledge_base_memory_uuid = str(uuid)
        try:
            memory_orm_object.save()
            logger.info(f"[document_embedder.embed_memory_sync] Memory ORM object saved successfully.")
        except Exception as e:
            logger.error(f"[document_embedder.embed_memory_sync] Error saving the memory ORM object into DB: {e}")
            error = f"[document_embedder.embed_memory_sync] Error saving the memory ORM object into DB: {e}"
            print(error)
    except Exception as e:
        logger.error(f"[document_embedder.embed_memory_sync] Error embedding the memory: {e}")
        error = f"[document_embedder.embed_memory_sync] Error embedding the memory: {e}"
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
            logger.error(f"[document_embedder.embed_document_helper] Error building the document ORM structure: {error}")
            return document_id, document_uuid, error
        logger.info(f"[document_embedder.embed_document_helper] Document ORM object created successfully.")

        document_weaviate_object, error = build_document_weaviate_structure(
            document=document,
            path=path,
            number_of_chunks=number_of_chunks
        )
        if error:
            logger.error(f"[document_embedder.embed_document_helper] Error building the document Weaviate structure: {error}")
            return document_id, document_uuid, error
        logger.info(f"[document_embedder.embed_document_helper] Document Weaviate object created successfully.")

        document_uuid, error = embed_document_sync(
            executor_params=executor_params,
            document_id=document_id,
            document_weaviate_object=document_weaviate_object,
            path=path
        )
        if error:
            logger.error(f"[document_embedder.embed_document_helper] Error embedding the document and saving the ORM object: {error}")
            return document_id, document_uuid, error
    except Exception as e:
        logger.error(f"[document_embedder.embed_document_helper] Error embedding the document: {e}")
        return f"[document_embedder.embed_document_helper] Error embedding the document: {e}"
    logger.info(f"[document_embedder.embed_document_helper] Document embedded successfully.")
    return document_id, document_uuid, error


def embed_memory_helper(executor_params: dict, number_of_chunks: int):
    from apps.datasource_knowledge_base.models import ContextHistoryKnowledgeBaseConnection
    memory_id, memory_uuid = None, None
    connection_id = executor_params["connection_id"]
    connection_orm_object = ContextHistoryKnowledgeBaseConnection.objects.get(id=connection_id)
    from apps.datasource_knowledge_base.utils import build_random_alphanumeric_string
    memory_name = build_random_alphanumeric_string(numeric_component=False)

    try:
        memory_id, error = build_memory_orm_structure(
            knowledge_base=connection_orm_object,
            memory_name=memory_name
        )
        if error:
            logger.error(f"[document_embedder.embed_memory_helper] Error building the memory ORM structure: {error}")
            return memory_id, memory_uuid, error
        logger.info(f"[document_embedder.embed_memory_helper] Memory ORM object created successfully.")

        memory_weaviate_object, error = build_memory_weaviate_structure(
            memory_name=memory_name,
            number_of_chunks=number_of_chunks
        )
        if error:
            logger.error(f"[document_embedder.embed_memory_helper] Error building the memory Weaviate structure: {error}")
            return memory_id, memory_uuid, error
        logger.info(f"[document_embedder.embed_memory_helper] Memory Weaviate object created successfully.")

        memory_uuid, error = embed_memory_sync(
            executor_params=executor_params,
            memory_id=memory_id,
            memory_weaviate_object=memory_weaviate_object
        )
        if error:
            logger.error(f"[document_embedder.embed_memory_helper] Error embedding the memory: {error}")
            return memory_id, memory_uuid, error

    except Exception as e:
        logger.error(f"[document_embedder.embed_memory_helper] Error embedding the memory: {e}")
        return f"[document_embedder.embed_memory_helper] Error embedding the memory: {e}"
    logger.info(f"[document_embedder.embed_memory_helper] Memory embedded successfully.")
    return memory_id, memory_uuid, error
