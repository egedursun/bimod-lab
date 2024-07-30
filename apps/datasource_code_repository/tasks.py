from celery import shared_task



@shared_task
def index_repository_helper(connection_id, document_paths):
    from apps.datasource_code_repository.models import CodeRepositoryConnection
    from apps._services.code_repository.code_repository_decoder import CodeRepositorySystemDecoder
    from apps.datasource_knowledge_base.models import DocumentProcessingLog, DocumentUploadStatusNames

    connection = CodeRepositoryConnection.objects.get(id=connection_id)
    executor = CodeRepositorySystemDecoder.get(connection=connection)
    ##################################################
    if isinstance(document_paths, str):
        document_paths = [document_paths]
    # Iterate through the documents
    print(f"Indexing {len(document_paths)} document(s)...")
    print(document_paths)
    for i, path in enumerate(document_paths):
        print(f"Indexing document [{i+1}] of [{len(document_paths)}] with path: {path}")
        try:
            # Get the file extension
            extension = path.split(".")[-1]
            print(f"Filename: {path.split('/')[-1]}")
            print(f"Identified file extension: {extension}")
            # Load the document
            print("Loading document...")
            document = executor.document_loader(file_path=path, file_type=extension)
            if not document:
                print(f"Error loading the document with path: {path}")
                add_document_upload_log(document_full_uri=path, log_name=DocumentUploadStatusNames.FAILED)
                continue
            add_document_upload_log(document_full_uri=path, log_name=DocumentUploadStatusNames.LOADED)

            # Chunk the document
            print("Preparing document for chunking...")
            chunks = executor.chunk_document(connection_id=executor.connection_object.id, document=document)
            if not chunks:
                print(f"Error chunking the document with path: {path}")
                add_document_upload_log(document_full_uri=path, log_name=DocumentUploadStatusNames.FAILED)
                continue
            add_document_upload_log(document_full_uri=path, log_name=DocumentUploadStatusNames.CHUNKED)

            print("Calculating number of chunks...")
            number_of_chunks = len(chunks) if chunks else 0
            print(f"Identified number of chunks: {number_of_chunks}")

            # Embed the document
            print("Embedding document...")
            doc_id, doc_uuid, error = executor.embed_document(
                document=document, path=path, number_of_chunks=number_of_chunks
            )
            add_document_upload_log(document_full_uri=path, log_name=DocumentUploadStatusNames.PROCESSED_DOCUMENT)

            print(f"Document ID: {doc_id}")
            if error or not doc_id or not doc_uuid:
                print(f"Error embedding the document with path: {path} - Error: {error}")
                add_document_upload_log(document_full_uri=path, log_name=DocumentUploadStatusNames.FAILED)
                continue

            # Embed the document chunks
            print("Embedding document chunks...")
            errors = executor.embed_document_chunks(chunks=chunks, path=path, document_id=doc_id,
                                                    document_uuid=doc_uuid)
            if errors:
                print(f"Error embedding at least one of the document chunks with the document path: {path} -"
                      f" Error: {errors}")
                add_document_upload_log(document_full_uri=path, log_name=DocumentUploadStatusNames.PARTIALLY_FAILED)
                continue
            add_document_upload_log(document_full_uri=path, log_name=DocumentUploadStatusNames.PROCESSED_CHUNKS)

            print(f"Document with path: {path} successfully indexed.")
            add_document_upload_log(document_full_uri=path, log_name=DocumentUploadStatusNames.COMPLETED)

        except Exception as e:
            print(f"Error indexing the document with path: {path} - Error: {e}")
            continue
    # make sure that the return statement is outside the loop
    return
