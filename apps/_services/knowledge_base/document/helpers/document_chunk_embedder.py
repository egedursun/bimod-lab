import datetime
import json


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
        id = chunk_orm_object.id
    except Exception as e:
        error = f"Error building the chunk ORM structure: {e}"

    return id, error


def build_chunk_weaviate_structure(chunk: dict, path: str,
                                   chunk_index: int,
                                   document_uuid: str):
    chunk_weaviate_object, error = None, None
    try:
        weav_chunk_document_file_name = str(path)
        weav_chunk_document_type = path.split(".")[-1]
        weav_chunk_number = chunk_index
        weav_chunk_content = chunk["page_content"]
        weav_chunk_metadata = json.dumps(chunk["metadata"], default=str, sort_keys=True)
        weav_chunk_created_at = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        chunk_weaviate_object = {
            "document_uuid": document_uuid,
            "chunk_document_file_name": weav_chunk_document_file_name,
            "chunk_document_type": weav_chunk_document_type,
            "chunk_number": weav_chunk_number,
            "chunk_content": weav_chunk_content,
            "chunk_metadata": weav_chunk_metadata,
            "created_at": weav_chunk_created_at
        }
    except Exception as e:
        error = f"Error building the chunk Weaviate structure: {e}"

    return chunk_weaviate_object, error


def embed_document_chunk_sync(executor_params,
                              chunk_id,
                              chunk_weaviate_object: dict,
                              path: str):
    from apps._services.knowledge_base.document.knowledge_base_decoder import KnowledgeBaseSystemDecoder
    from apps.datasource_knowledge_base.models import (DocumentKnowledgeBaseConnection, KnowledgeBaseDocumentChunk)

    # Retrieve connection details
    connection_id = executor_params["connection_id"]
    connection_orm_object = DocumentKnowledgeBaseConnection.objects.get(id=connection_id)

    # Re-initialize the executor
    executor = KnowledgeBaseSystemDecoder.get(connection=connection_orm_object)
    c = executor.connect_c()
    if not c:
        print(f"[Chunk Embedder]: Error while connecting to Weaviate")
    error = None
    try:
        # Save the object to Weaviate
        chunk_class_name = f"{executor.connection_object.class_name}Chunks"
        collection = c.collections.get(chunk_class_name)
        uuid = collection.data.insert(
            properties=chunk_weaviate_object
        )

        if not uuid:
            error = "Error inserting the chunk into Weaviate"

        # Save the object to the ORM
        chunk_orm_object = KnowledgeBaseDocumentChunk.objects.filter(id=chunk_id).first()
        chunk_orm_object.knowledge_base_uuid = str(uuid)
        chunk_orm_object.save()

        # add the chunk to the document chunks
        document = chunk_orm_object.document
        document.document_chunks.add(chunk_orm_object)
        document.save()

    except Exception as e:
        print(f"Error embedding the chunk: {e}")
        error = f"Error embedding the chunk: {e}"
    print(f"Successfully embedded the chunk...")
    return error


def embed_document_chunks_helper(executor_params, chunks: list, path: str, document_id: int,
                                 document_uuid: str):
    from apps.datasource_knowledge_base.models import DocumentKnowledgeBaseConnection, DocumentUploadStatusNames
    from apps.datasource_knowledge_base.tasks import add_document_upload_log

    errors = []
    # Retrieve connection object
    connection_id = executor_params["connection_id"]
    connection_orm_object = DocumentKnowledgeBaseConnection.objects.get(id=connection_id)
    try:
        for i, chunk in enumerate(chunks):
            print(f"Building ORM and Weaviate structures for chunk: {i}")
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
                chunk_weaviate_object=document_weaviate_object,
                path=path
            )
            if error:
                errors.append(error)
                continue
        add_document_upload_log(document_full_uri=path, log_name=DocumentUploadStatusNames.EMBEDDED_CHUNKS)
        add_document_upload_log(document_full_uri=path, log_name=DocumentUploadStatusNames.SAVED_CHUNKS)

    except Exception as e:
        errors.append(f"Error embedding the chunks: {e}")
    return errors
