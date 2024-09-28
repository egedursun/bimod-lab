import datetime
import json

from apps.datasource_knowledge_base.utils import DocumentUploadStatusNames


def build_chunk_orm_structure(chunk: dict,
                              knowledge_base,
                              document_id: int,
                              document_uuid: str,
                              path: str,
                              chunk_index: int):
    from apps.datasource_knowledge_base.models import KnowledgeBaseDocumentChunk
    from apps.datasource_knowledge_base.models import KnowledgeBaseDocument
    id, error = None, None
    try:
        chunk_knowledge_base = knowledge_base
        chunk_document = KnowledgeBaseDocument.objects.filter(id=document_id).first()
        chunk_document_uuid = document_uuid
        chunk_document_type = path.split(".")[-1]
        chunk_number = chunk_index
        chunk_content = chunk["page_content"]
        chunk_metadata = chunk["metadata"]
        chunk_document_uri = path

        chunk_orm_object = KnowledgeBaseDocumentChunk.objects.create(
            knowledge_base=chunk_knowledge_base,
            chunk_document_type=chunk_document_type,
            chunk_number=chunk_number,
            chunk_content=chunk_content,
            chunk_metadata=chunk_metadata,
            chunk_document_uri=chunk_document_uri,
            document=chunk_document,
            document_uuid=chunk_document_uuid
        )
        print(f"[document_chunk_embedder.build_chunk_orm_structure] Chunk ORM object created.")
        id = chunk_orm_object.id
    except Exception as e:
        error = f"[document_chunk_embedder.build_chunk_orm_structure] Error building the chunk ORM structure: {e}"
        print(error)
    return id, error


def build_memory_chunk_orm_structure(chunk: str, knowledge_base, memory_id: int, memory_uuid: str,
                                        chunk_index: int):
    from apps.datasource_knowledge_base.models import ContextHistoryMemoryChunk
    from apps.datasource_knowledge_base.models import ContextHistoryMemory
    id, error = None, None
    try:
        context_history_base = knowledge_base
        memory = ContextHistoryMemory.objects.filter(id=memory_id).first()
        knowledge_base_memory_uuid = memory_uuid

        chunk_orm_object = ContextHistoryMemoryChunk.objects.create(
            memory=memory,
            chunk_number=chunk_index,
            chunk_content=chunk,
            knowledge_base_memory_uuid=knowledge_base_memory_uuid,
            context_history_base=context_history_base,
        )
        id = chunk_orm_object.id
        print(f"[document_chunk_embedder.build_memory_chunk_orm_structure] Memory chunk ORM object created.")
    except Exception as e:
        error = f"[document_chunk_embedder.build_memory_chunk_orm_structure] Error building the chunk ORM structure: {e}"
        print(error)
    return id, error


def build_chunk_weaviate_structure(chunk: dict, path: str,
                                   chunk_index: int,
                                   document_uuid: str):
    chunk_weaviate_object, error = None, None
    try:
        weaviate_chunk_document_file_name = str(path)
        weaviate_chunk_document_type = path.split(".")[-1]
        weaviate_chunk_number = chunk_index
        weaviate_chunk_content = chunk["page_content"]
        weaviate_chunk_metadata = json.dumps(chunk["metadata"], default=str, sort_keys=True)
        weaviate_chunk_created_at = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        chunk_weaviate_object = {
            "document_uuid": document_uuid,
            "chunk_document_file_name": weaviate_chunk_document_file_name,
            "chunk_document_type": weaviate_chunk_document_type,
            "chunk_number": weaviate_chunk_number,
            "chunk_content": weaviate_chunk_content,
            "chunk_metadata": weaviate_chunk_metadata,
            "created_at": weaviate_chunk_created_at
        }
        print(f"[document_chunk_embedder.build_chunk_weaviate_structure] Chunk Weaviate object created.")
    except Exception as e:
        error = f"[document_chunk_embedder.build_chunk_weaviate_structure] Error building the chunk Weaviate structure: {e}"
        print(error)
    return chunk_weaviate_object, error


def build_memory_chunk_weaviate_structure(memory, chunk: str, chunk_index: int, memory_uuid: str):
    chunk_weaviate_object, error = None, None
    try:
        weaviate_chunk_number = chunk_index
        weaviate_chunk_content = chunk
        weaviate_chunk_created_at = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        chunk_weaviate_object = {
            "memory_uuid": memory_uuid,
            "memory_name": memory.memory_name,
            "chunk_number": weaviate_chunk_number,
            "chunk_content": weaviate_chunk_content,
            "created_at": weaviate_chunk_created_at
        }
        print(f"[document_chunk_embedder.build_memory_chunk_weaviate_structure] Memory chunk Weaviate object created.")
    except Exception as e:
        error = f"[document_chunk_embedder.build_memory_chunk_weaviate_structure] Error building the memory chunk Weaviate structure: {e}"
        print(error)
    return chunk_weaviate_object, error


def embed_document_chunk_sync(executor_params, chunk_id, chunk_weaviate_object: dict):
    from apps._services.knowledge_base.document.knowledge_base_decoder import KnowledgeBaseSystemDecoder
    from apps.datasource_knowledge_base.models import (DocumentKnowledgeBaseConnection, KnowledgeBaseDocumentChunk)

    # Retrieve connection details
    connection_id = executor_params["connection_id"]
    connection_orm_object = DocumentKnowledgeBaseConnection.objects.get(id=connection_id)

    # Re-initialize the executor
    executor = KnowledgeBaseSystemDecoder.get(connection=connection_orm_object)
    c = executor.connect_c()
    if not c:
        print(f"[Chunk Embedder.embed_document_chunk_sync]: Error while connecting to Weaviate")
    print(f"[Chunk Embedder.embed_document_chunk_sync]: Connected to Weaviate successfully.")

    error = None
    try:
        # Save the object to Weaviate
        chunk_class_name = f"{executor.connection_object.class_name}Chunks"
        collection = c.collections.get(chunk_class_name)
        uuid = collection.data.insert(properties=chunk_weaviate_object)
        print(f"[Chunk Embedder.embed_document_chunk_sync]: Chunk inserted successfully.")
        if not uuid:
            error = "Error inserting the chunk into Weaviate"

        # Save the object to the ORM
        chunk_orm_object = KnowledgeBaseDocumentChunk.objects.filter(id=chunk_id).first()
        chunk_orm_object.chunk_uuid = str(uuid)
        chunk_orm_object.save()
        print(f"[Chunk Embedder.embed_document_chunk_sync]: Chunk saved to the ORM successfully.")

        # add the chunk to the document chunks
        document = chunk_orm_object.document
        document.document_chunks.add(chunk_orm_object)
        document.save()
        print(f"[Chunk Embedder.embed_document_chunk_sync]: Chunk saved to the ORM successfully.")

    except Exception as e:
        error = f"[document_chunk_embedder.embed_document_chunk_sync] Error embedding the chunk: {e}"
        print(error)
    print(f"[Chunk Embedder.embed_document_chunk_sync]: Exiting the function.")
    return error


def embed_memory_chunk_sync(executor_params, chunk_id, chunk_weaviate_object: dict):
    from apps.datasource_knowledge_base.models import ContextHistoryKnowledgeBaseConnection, ContextHistoryMemoryChunk
    from apps._services.knowledge_base.memory.memory_executor import MemoryExecutor
    connection_id = executor_params["connection_id"]
    connection_orm_object = ContextHistoryKnowledgeBaseConnection.objects.get(id=connection_id)
    executor = MemoryExecutor(connection=connection_orm_object)
    c = executor.connect_c()
    if not c:
        print(f"[Memory Chunk Embedder.embed_memory_chunk_sync]: Error while connecting to Weaviate")
    print(f"[Memory Chunk Embedder.embed_memory_chunk_sync]: Connected to Weaviate successfully.")

    error = None
    try:
        # Save the object to Weaviate
        chunk_class_name = f"{executor.connection_object.class_name}Chunks"
        collection = c.collections.get(chunk_class_name)
        uuid = collection.data.insert(properties=chunk_weaviate_object)
        print(f"[Memory Chunk Embedder.embed_memory_chunk_sync]: Memory chunk inserted successfully.")
        if not uuid:
            error = "Error inserting the memory chunk into Weaviate"

        # Save the object to the ORM
        chunk_orm_object = ContextHistoryMemoryChunk.objects.filter(id=chunk_id).first()
        chunk_orm_object.chunk_uuid = str(uuid)
        chunk_orm_object.save()
        print(f"[Memory Chunk Embedder.embed_memory_chunk_sync]: Memory chunk saved to the ORM successfully.")

        # add the chunk to the document chunks
        memory_object = chunk_orm_object.memory
        memory_object.memory_chunks.add(chunk_orm_object)
        memory_object.save()
    except Exception as e:
        error = f"[document_chunk_embedder.embed_memory_chunk_sync] Error embedding the memory chunk: {e}"
        print(error)
    return error


def embed_document_chunks_helper(executor_params, chunks: list, path: str, document_id: int,
                                 document_uuid: str):
    from apps.datasource_knowledge_base.models import DocumentKnowledgeBaseConnection
    from apps.datasource_knowledge_base.tasks import add_document_upload_log
    errors = []
    connection_id = executor_params["connection_id"]
    connection_orm_object = DocumentKnowledgeBaseConnection.objects.get(id=connection_id)
    print(f"[document_chunk_embedder.embed_document_chunks_helper] Embedding chunks...")
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
            error = embed_document_chunk_sync(
                executor_params=executor_params,
                chunk_id=chunk_id,
                chunk_weaviate_object=document_weaviate_object
            )
            if error:
                errors.append(error)
                continue
        add_document_upload_log(document_full_uri=path, log_name=DocumentUploadStatusNames.EMBEDDED_CHUNKS)
        add_document_upload_log(document_full_uri=path, log_name=DocumentUploadStatusNames.SAVED_CHUNKS)
    except Exception as e:
        errors.append(f"[document_chunk_embedder.embed_document_chunks_helper] Error embedding the chunks: {e}")
    print(f"[document_chunk_embedder.embed_document_chunks_helper] Exiting the function.")
    return errors


def embed_memory_chunks_helper(executor_params, chunks: list, memory_id: int, memory_uuid: str):
    from apps.datasource_knowledge_base.models import ContextHistoryKnowledgeBaseConnection
    from apps.datasource_knowledge_base.models import ContextHistoryMemory
    errors = []
    connection_id = executor_params["connection_id"]
    connection_orm_object = ContextHistoryKnowledgeBaseConnection.objects.get(id=connection_id)
    memory = ContextHistoryMemory.objects.filter(id=memory_id).first()
    try:
        for i, chunk in enumerate(chunks):
            chunk_id, error = build_memory_chunk_orm_structure(
                knowledge_base=connection_orm_object,
                chunk=chunk,
                chunk_index=i,
                memory_id=memory_id,
                memory_uuid=memory_uuid
            )
            if error:
                errors.append(error)
                continue

            chunk_weaviate_object, error = build_memory_chunk_weaviate_structure(
                memory=memory,
                chunk=chunk,
                chunk_index=i,
                memory_uuid=memory_uuid
            )
            if error:
                errors.append(error)
                continue
            error = embed_memory_chunk_sync(
                executor_params=executor_params,
                chunk_id=chunk_id,
                chunk_weaviate_object=chunk_weaviate_object
            )
            if error:
                errors.append(error)
                continue
    except Exception as e:
        errors.append(f"[document_chunk_embedder.embed_memory_chunks_helper] Error embedding the memory chunks: {e}")
    print(f"[document_chunk_embedder.embed_memory_chunks_helper] Exiting the function.")
    return errors
