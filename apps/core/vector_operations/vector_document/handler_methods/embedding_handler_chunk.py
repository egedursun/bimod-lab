#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: document_chunk_embedder.py
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

import datetime
import json

from apps.datasource_knowledge_base.utils import VectorStoreDocProcessingStatusNames


def factory_chunk_orm_build(chunk: dict,
                            knowledge_base,
                            document_id: int,
                            document_uuid: str,
                            path: str,
                            chunk_index: int):
    from apps.datasource_knowledge_base.models import KnowledgeBaseDocumentChunk
    from apps.datasource_knowledge_base.models import KnowledgeBaseDocument
    _id, error = None, None
    try:
        chunk_vector_store = knowledge_base
        chunk_doc = KnowledgeBaseDocument.objects.filter(id=document_id).first()
        chunk_doc_uuid = document_uuid
        chunk_doc_type = path.split(".")[-1]
        chunk_no = chunk_index
        chunk_ingredient = chunk["page_content"]
        chunk_metadata = chunk["metadata"]
        chunk_doc_uri = path
        chunk_orm_object = KnowledgeBaseDocumentChunk.objects.create(
            knowledge_base=chunk_vector_store, chunk_document_type=chunk_doc_type, chunk_number=chunk_no,
            chunk_content=chunk_ingredient, chunk_metadata=chunk_metadata, chunk_document_uri=chunk_doc_uri,
            document=chunk_doc, document_uuid=chunk_doc_uuid
        )
        _id = chunk_orm_object.id
    except Exception as e:
        pass
    return _id, error


def factory_intra_context_memory_chunk_orm_build(chunk: str, knowledge_base, memory_id: int, memory_uuid: str,
                                                 chunk_index: int):
    from apps.datasource_knowledge_base.models import ContextHistoryMemoryChunk
    from apps.datasource_knowledge_base.models import ContextHistoryMemory
    _id, error = None, None
    try:
        vector_store = knowledge_base
        memory_instance = ContextHistoryMemory.objects.filter(id=memory_id).first()
        intra_context_memory_uuid = memory_uuid
        chunk_orm_object = ContextHistoryMemoryChunk.objects.create(
            memory=memory_instance, chunk_number=chunk_index, chunk_content=chunk,
            knowledge_base_memory_uuid=intra_context_memory_uuid, context_history_base=vector_store,
        )
        _id = chunk_orm_object.id
    except Exception as e:
        pass
    return _id, error


def factory_chunk_weaviate_build(chunk: dict, path: str,
                                 chunk_index: int,
                                 document_uuid: str):
    weaviate_object_instance_chunk, error = None, None
    try:
        weaviate_chunk_doc_file_name = str(path)
        weaviate_chunk_doc_type = path.split(".")[-1]
        weaviate_chunk_no = chunk_index
        weaviate_chunk_ingredient = chunk["page_content"]
        weaviate_chunk_metadata = json.dumps(chunk["metadata"], default=str, sort_keys=True)
        weaviate_chunk_created_at = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        weaviate_object_instance_chunk = {
            "document_uuid": document_uuid, "chunk_document_file_name": weaviate_chunk_doc_file_name,
            "chunk_document_type": weaviate_chunk_doc_type, "chunk_number": weaviate_chunk_no,
            "chunk_content": weaviate_chunk_ingredient, "chunk_metadata": weaviate_chunk_metadata,
            "created_at": weaviate_chunk_created_at
        }
    except Exception as e:
        pass
    return weaviate_object_instance_chunk, error


def factory_intra_context_memory_chunk_weaviate_build(memory, chunk: str, chunk_index: int, memory_uuid: str):
    weaviate_memory_instance_chunk, error = None, None
    try:
        weaviate_chunk_no = chunk_index
        weaviate_chunk_igredient = chunk
        weaviate_chunk_created_at = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        weaviate_memory_instance_chunk = {
            "memory_uuid": memory_uuid, "memory_name": memory.memory_name, "chunk_number": weaviate_chunk_no,
            "chunk_content": weaviate_chunk_igredient, "created_at": weaviate_chunk_created_at
        }
    except Exception as e:
        pass
    return weaviate_memory_instance_chunk, error


def factory_embed_document_chunk_synchronized(executor_params, chunk_id, chunk_weaviate_object: dict):
    from apps.core.vector_operations.vector_document.vector_store_decoder import KnowledgeBaseSystemDecoder
    from apps.datasource_knowledge_base.models import (DocumentKnowledgeBaseConnection, KnowledgeBaseDocumentChunk)
    c_id = executor_params["connection_id"]
    c_orm = DocumentKnowledgeBaseConnection.objects.get(id=c_id)
    x = KnowledgeBaseSystemDecoder.get(connection=c_orm)
    c = x.connect_c()
    if not c:
        pass
    pass

    error = None
    try:
        class_name = f"{x.connection_object.class_name}Chunks"
        collection = c.collections.get(class_name)
        uuid = collection.data.insert(properties=chunk_weaviate_object)
        if not uuid:
            error = "Error inserting the chunk."
            pass
        chunk_orm = KnowledgeBaseDocumentChunk.objects.filter(id=chunk_id).first()
        chunk_orm.chunk_uuid = str(uuid)
        chunk_orm.save()
        document = chunk_orm.document
        document.document_chunks.add(chunk_orm)
        document.save()
    except Exception as e:
        pass
    return error


def factory_embed_memory_chunk_synchronized(executor_params, chunk_id, chunk_weaviate_object: dict):
    from apps.datasource_knowledge_base.models import ContextHistoryKnowledgeBaseConnection, ContextHistoryMemoryChunk
    from apps.core.vector_operations.intra_context_memory.memory_executor import IntraContextMemoryExecutor
    c_id = executor_params["connection_id"]
    c_orm = ContextHistoryKnowledgeBaseConnection.objects.get(id=c_id)
    x = IntraContextMemoryExecutor(connection=c_orm)
    c = x.connect_c()
    if not c:
        pass
    pass

    error = None
    try:
        class_name = f"{x.connection_object.class_name}Chunks"
        collection = c.collections.get(class_name)
        uuid = collection.data.insert(properties=chunk_weaviate_object)
        if not uuid:
            error = "Error inserting the memory chunk."
            pass
        chunk_orm = ContextHistoryMemoryChunk.objects.filter(id=chunk_id).first()
        chunk_orm.chunk_uuid = str(uuid)
        chunk_orm.save()
        memory_object = chunk_orm.memory
        memory_object.memory_chunks.add(chunk_orm)
        memory_object.save()
    except Exception as e:
        pass
    return error


def factory_embed_document_chunks_handler(executor_params, chunks: list, path: str, document_id: int,
                                          document_uuid: str):
    from apps.datasource_knowledge_base.models import DocumentKnowledgeBaseConnection
    from apps.datasource_knowledge_base.tasks import add_vector_store_doc_loaded_log
    errors = []
    c_id = executor_params["connection_id"]
    c_orm = DocumentKnowledgeBaseConnection.objects.get(id=c_id)
    try:
        for i, ch in enumerate(chunks):
            ch_id, error = factory_chunk_orm_build(
                knowledge_base=c_orm, chunk=ch, path=path, chunk_index=i, document_id=document_id,
                document_uuid=document_uuid
            )
            if error:
                errors.append(error)
                continue
            document_weaviate_object, error = factory_chunk_weaviate_build(
                chunk=ch, path=path, chunk_index=i, document_uuid=document_uuid
            )
            if error:
                errors.append(error)
                continue
            error = factory_embed_document_chunk_synchronized(
                executor_params=executor_params, chunk_id=ch_id, chunk_weaviate_object=document_weaviate_object
            )
            if error:
                errors.append(error)
                continue
        add_vector_store_doc_loaded_log(document_full_uri=path, log_name=VectorStoreDocProcessingStatusNames.EMBEDDED_CHUNKS)
        add_vector_store_doc_loaded_log(document_full_uri=path, log_name=VectorStoreDocProcessingStatusNames.SAVED_CHUNKS)
    except Exception as e:
        pass
    return errors


def factory_embed_memory_chunks_handler(executor_params, chunks: list, memory_id: int, memory_uuid: str):
    from apps.datasource_knowledge_base.models import ContextHistoryKnowledgeBaseConnection
    from apps.datasource_knowledge_base.models import ContextHistoryMemory
    errors = []
    c_id = executor_params["connection_id"]
    c_orm = ContextHistoryKnowledgeBaseConnection.objects.get(id=c_id)
    memory = ContextHistoryMemory.objects.filter(id=memory_id).first()
    try:
        for i, ch in enumerate(chunks):
            ch_id, error = factory_intra_context_memory_chunk_orm_build(
                knowledge_base=c_orm, chunk=ch,  chunk_index=i, memory_id=memory_id, memory_uuid=memory_uuid
            )
            if error:
                errors.append(error)
                continue

            chunk_weaviate_object, error = factory_intra_context_memory_chunk_weaviate_build(
                memory=memory, chunk=ch, chunk_index=i, memory_uuid=memory_uuid
            )
            if error:
                errors.append(error)
                continue
            error = factory_embed_memory_chunk_synchronized(
                executor_params=executor_params, chunk_id=ch_id, chunk_weaviate_object=chunk_weaviate_object
            )
            if error:
                errors.append(error)
                continue
    except Exception as e:
        errors.append(f"Error embedding the chunks: {e}")
    return errors
