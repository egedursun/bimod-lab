import datetime
import json


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

        # Prepare the object but don't save it yet
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
    except Exception as e:
        error = f"Error building the document ORM structure: {e}"

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
    except Exception as e:
        error = f"Error building the document Weaviate structure: {e}"

    return document_weaviate_object, error


def embed_document_sync(executor_params, document_id, document_weaviate_object: dict):
    from apps._services.knowledge_base.document.knowledge_base_decoder import KnowledgeBaseSystemDecoder
    from apps.datasource_knowledge_base.models import DocumentKnowledgeBaseConnection
    from apps.datasource_knowledge_base.models import KnowledgeBaseDocument

    # Retrieve connection details
    connection_id = executor_params["connection_id"]
    connection_orm_object = DocumentKnowledgeBaseConnection.objects.get(id=connection_id)

    # Re-initialize the executor
    executor = KnowledgeBaseSystemDecoder.get(connection=connection_orm_object)
    c = executor.client
    error = None
    uuid = None

    try:
        # Save the object to Weaviate
        collection = c.collections.get(executor.connection_object.class_name)
        uuid = collection.data.insert(properties=document_weaviate_object)

        if not uuid:
            error = "Error inserting the document into Weaviate"

        document_orm_object = KnowledgeBaseDocument.objects.get(id=document_id)
        document_orm_object.knowledge_base_uuid = str(uuid)
        try:
            document_orm_object.save()
        except Exception as e:
            error = f"Error saving the document ORM object into DB: {e}"
            print("DB Save error.")

    except Exception as e:
        error = f"Error embedding the document: {e}"

    return uuid, error


def embed_document_helper(executor_params: dict, document: dict, path: str, number_of_chunks: int):
    from apps.datasource_knowledge_base.models import DocumentKnowledgeBaseConnection

    # Retrieve connection object
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
            return document_id, error

        document_weaviate_object, error = build_document_weaviate_structure(
            document=document,
            path=path,
            number_of_chunks=number_of_chunks
        )
        if error:
            return document_id, error

        document_uuid, error = embed_document_sync(
            executor_params=executor_params,
            document_id=document_id,
            document_weaviate_object=document_weaviate_object
        )
        if error:
            return document_id, document_uuid, error

    except Exception as e:
        return f"Error embedding the document: {e}"
    return document_id, document_uuid, error
