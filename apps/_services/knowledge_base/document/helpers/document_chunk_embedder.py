import datetime
import json


def build_chunk_orm_structure(chunk: dict,
                              knowledge_base,
                              document_id: int,
                              path: str,
                              chunk_index: int):
    from apps.datasource_knowledge_base.models import KnowledgeBaseDocumentChunk
    from apps.datasource_knowledge_base.models import KnowledgeBaseDocument
    id, error = None, None
    try:
        chunk_knowledge_base = knowledge_base
        chunk_document = KnowledgeBaseDocument.objects.filter(id=document_id).first()
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
            document=chunk_document
        )
        id = chunk_orm_object.id
    except Exception as e:
        error = f"Error building the chunk ORM structure: {e}"

    return id, error


def build_chunk_weaviate_structure(chunk: dict, path: str,
                                   chunk_index: int):
    chunk_weaviate_object, error = None, None
    try:
        weav_chunk_document_type = path.split(".")[-1]
        weav_chunk_number = chunk_index
        weav_chunk_content = chunk["page_content"]
        weav_chunk_metadata = json.dumps(chunk["metadata"], default=str, sort_keys=True)
        weav_chunk_created_at = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        chunk_weaviate_object = {
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
                              chunk_weaviate_object: dict):
    from apps._services.knowledge_base.document.knowledge_base_decoder import KnowledgeBaseSystemDecoder
    from apps.datasource_knowledge_base.models import DocumentKnowledgeBaseConnection
    from apps.datasource_knowledge_base.models import KnowledgeBaseDocumentChunk

    # Retrieve connection details
    connection_id = executor_params["connection_id"]
    connection_orm_object = DocumentKnowledgeBaseConnection.objects.get(id=connection_id)

    # Re-initialize the executor
    executor = KnowledgeBaseSystemDecoder.get(connection=connection_orm_object)
    c = executor.client
    error = None
    try:
        # Save the object to Weaviate
        chunk_class_name = f"{executor.connection_object.class_name}Chunks"
        collection = c.collections.get(chunk_class_name)
        uuid = collection.data.insert(
            properties=chunk_weaviate_object
        )
        executor.close_connection()

        if not uuid:
            error = "Error inserting the chunk into Weaviate"

        # Save the object to the ORM
        chunk_orm_object = KnowledgeBaseDocumentChunk.objects.filter(id=chunk_id)
        chunk_orm_object.knowledge_base_uuid = str(uuid)
        chunk_orm_object.save()

        # add the chunk to the document chunks
        document = chunk_orm_object.document
        document.chunks.add(chunk_orm_object)
        document.save()

    except Exception as e:
        error = f"Error embedding the chunk: {e}"
    return error


def embed_document_chunks_helper(executor_params, chunks: list, path: str, document_id: int):
    from apps.datasource_knowledge_base.models import DocumentKnowledgeBaseConnection

    errors = []
    # Retrieve connection object
    connection_id = executor_params["connection_id"]
    connection_orm_object = DocumentKnowledgeBaseConnection.objects.get(id=connection_id)
    try:
        for i, chunk in enumerate(chunks):
            chunk_id, error = build_chunk_orm_structure(
                knowledge_base=connection_orm_object,
                chunk=chunk,
                path=path,
                chunk_index=i,
                document_id=document_id
            )
            if error:
                errors.append(error)
                continue

            document_weaviate_object, error = build_chunk_weaviate_structure(
                chunk=chunk,
                path=path,
                chunk_index=i
            )
            if error:
                errors.append(error)
                continue

            error = embed_document_chunk_sync(
                executor_params=executor_params,
                chunk_id=chunk_id,
                chunk_weaviate_object=document_weaviate_object
            )
            if error:
                errors.append(error)
                continue

    except Exception as e:
        errors.append(f"Error embedding the chunks: {e}")
    print("Items successfully processed: (", (len(chunks) - len(errors)), "/", len(chunks), ")")
    return errors
