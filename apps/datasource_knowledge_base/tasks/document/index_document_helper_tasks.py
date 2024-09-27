from celery import shared_task


@shared_task
def index_document_helper(connection_id, document_paths):
    from apps.datasource_knowledge_base.models import DocumentKnowledgeBaseConnection
    from apps._services.knowledge_base.document.knowledge_base_decoder import KnowledgeBaseSystemDecoder
    from apps.datasource_knowledge_base.utils import DocumentUploadStatusNames
    from apps.datasource_knowledge_base.tasks import add_document_upload_log

    connection = DocumentKnowledgeBaseConnection.objects.get(id=connection_id)
    executor = KnowledgeBaseSystemDecoder.get(connection=connection)
    if isinstance(document_paths, str):
        document_paths = [document_paths]
    # Iterate through the documents
    print(f"[tasks.index_document_helper] Indexing {len(document_paths)} document(s)...")
    print(document_paths)
    for i, path in enumerate(document_paths):
        try:
            # Get the file extension
            extension = path.split(".")[-1]
            # Load the document
            document = executor.document_loader(file_path=path, file_type=extension)
            if not document:
                print(f"[tasks.index_document_helper] Error loading the document with path: {path}")
                add_document_upload_log(document_full_uri=path, log_name=DocumentUploadStatusNames.FAILED)
                continue
            add_document_upload_log(document_full_uri=path, log_name=DocumentUploadStatusNames.LOADED)

            # Chunk the document
            chunks = executor.chunk_document(connection_id=executor.connection_object.id, document=document)
            if not chunks:
                print(f"[tasks.index_document_helper] Error chunking the document with path: {path}")
                add_document_upload_log(document_full_uri=path, log_name=DocumentUploadStatusNames.FAILED)
                continue
            add_document_upload_log(document_full_uri=path, log_name=DocumentUploadStatusNames.CHUNKED)

            number_of_chunks = len(chunks) if chunks else 0
            print(f"[tasks.index_document_helper] Identified number of chunks: {number_of_chunks}")

            # Embed the document
            doc_id, doc_uuid, error = executor.embed_document(
                document=document, path=path, number_of_chunks=number_of_chunks
            )
            add_document_upload_log(document_full_uri=path, log_name=DocumentUploadStatusNames.PROCESSED_DOCUMENT)

            if error or not doc_id or not doc_uuid:
                print(f"[tasks.index_document_helper] Error embedding the document with path: {path} - Error: {error}")
                add_document_upload_log(document_full_uri=path, log_name=DocumentUploadStatusNames.FAILED)
                continue

            # Embed the document chunks
            errors = executor.embed_document_chunks(chunks=chunks, path=path, document_id=doc_id,
                                                    document_uuid=doc_uuid)
            if errors:
                print(
                    f"[tasks.index_document_helper] Error embedding at least one of the document chunks with the document path: {path} -"
                    f" Error: {errors}")
                add_document_upload_log(document_full_uri=path, log_name=DocumentUploadStatusNames.PARTIALLY_FAILED)
                continue
            add_document_upload_log(document_full_uri=path, log_name=DocumentUploadStatusNames.PROCESSED_CHUNKS)

            print(f"[tasks.index_document_helper] Document with path: {path} successfully indexed.")
            add_document_upload_log(document_full_uri=path, log_name=DocumentUploadStatusNames.COMPLETED)

        except Exception as e:
            print(f"[tasks.index_document_helper] Error indexing the document with path: {path} - Error: {e}")
            add_document_upload_log(document_full_uri=path, log_name=DocumentUploadStatusNames.FAILED)
            continue
    # make sure that the return statement is outside the loop
    return
