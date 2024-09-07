
from celery import shared_task
from langchain_text_splitters import RecursiveCharacterTextSplitter

from apps._services.codebase.helpers.repository_chunk_embedder import embed_repository_chunks_helper
from apps._services.codebase.helpers.repository_embedder import embed_repository_helper

MEMORY_DEFAULT_CHUNK_SIZE = 1000
MEMORY_DEFAULT_CHUNK_OVERLAP = 200


# INDEX
def add_repository_upload_log(document_full_uri, log_name):
    from apps.datasource_codebase.models import RepositoryProcessingLog
    RepositoryProcessingLog.objects.create(
        repository_full_uri=document_full_uri,
        log_message=log_name
    )


@shared_task
def index_repository_helper(connection_id, document_paths):
    from apps.datasource_codebase.models import CodeRepositoryStorageConnection
    from apps._services.codebase.codebase_decoder import CodeBaseDecoder
    from apps.datasource_codebase.models import RepositoryUploadStatusNames

    connection = CodeRepositoryStorageConnection.objects.get(id=connection_id)
    executor = CodeBaseDecoder.get(connection=connection)
    if isinstance(document_paths, str):
        document_paths = [document_paths]
    # Iterate through the repositories
    print(f"[tasks.index_repository_helper] Indexing {len(document_paths)} repository(s)...")
    print(document_paths)
    for i, path in enumerate(document_paths):
        try:
            # Load the repository
            accumulated_document = executor.repository_loader(file_path=path)
            if not accumulated_document:
                print(f"[tasks.index_repository_helper] Error loading the repository with path: {path}")
                add_repository_upload_log(document_full_uri=path, log_name=RepositoryUploadStatusNames.FAILED)
                continue
            add_repository_upload_log(document_full_uri=path, log_name=RepositoryUploadStatusNames.LOADED)

            # Chunk the document
            chunks = executor.chunk_repository(connection_id=executor.connection_object.id, document=accumulated_document)
            if not chunks:
                print(f"[tasks.index_repository_helper] Error chunking the repository with path: {path}")
                add_repository_upload_log(document_full_uri=path, log_name=RepositoryUploadStatusNames.FAILED)
                continue
            add_repository_upload_log(document_full_uri=path, log_name=RepositoryUploadStatusNames.CHUNKED)

            number_of_chunks = len(chunks) if chunks else 0
            print(f"[tasks.index_repository_helper] Identified number of chunks: {number_of_chunks}")

            # Embed the repository
            doc_id, doc_uuid, error = executor.embed_repository(
                document=accumulated_document, path=path, number_of_chunks=number_of_chunks
            )
            add_repository_upload_log(document_full_uri=path, log_name=RepositoryUploadStatusNames.PROCESSED_DOCUMENT)

            if error or not doc_id or not doc_uuid:
                print(f"[tasks.index_repository_helper] Error embedding the repository with path: {path} - Error: {error}")
                add_repository_upload_log(document_full_uri=path, log_name=RepositoryUploadStatusNames.FAILED)
                continue

            # Embed the document chunks
            errors = executor.embed_repository_chunks(chunks=chunks, path=path, document_id=doc_id,
                                                    document_uuid=doc_uuid)
            if errors:
                print(
                    f"[tasks.index_repository_helper] Error embedding at least one of the repository chunks with the repository path: {path} -"
                    f" Error: {errors}")
                add_repository_upload_log(document_full_uri=path, log_name=RepositoryUploadStatusNames.PARTIALLY_FAILED)
                continue
            add_repository_upload_log(document_full_uri=path, log_name=RepositoryUploadStatusNames.PROCESSED_CHUNKS)

            print(f"[tasks.index_repository_helper] Repository with path: {path} successfully indexed.")
            add_repository_upload_log(document_full_uri=path, log_name=RepositoryUploadStatusNames.COMPLETED)

        except Exception as e:
            print(f"[tasks.index_repository_helper] Error indexing the repository with path: {path} - Error: {e}")
            add_repository_upload_log(document_full_uri=path, log_name=RepositoryUploadStatusNames.FAILED)
            continue
    # make sure that the return statement is outside the loop
    return


# EMBEDDER
def embed_repository_data(executor_params, document, path, number_of_chunks):
    doc_id, doc_uuid = None, None
    try:
        doc_id, doc_uuid, error = embed_repository_helper(
            executor_params=executor_params,
            document=document,
            path=path,
            number_of_chunks=number_of_chunks
        )
    except Exception as e:
        error = f"[tasks.embed_repository_data] Error embedding the repository: {e}"
    return doc_id, doc_uuid, error


def embed_repository_chunks(executor_params, chunks, path, document_id, document_uuid):
    try:
        error = embed_repository_chunks_helper(
            executor_params=executor_params,
            chunks=chunks,
            path=path,
            document_id=document_id,
            document_uuid=document_uuid
        )
    except Exception as e:
        error = f"[tasks.embed_repository_chunks] Error embedding the repository chunks: {e}"
    return error


# CHUNKERS
def split_repository_into_chunks(connection_id, doc):
    from apps.datasource_codebase.models import CodeRepositoryStorageConnection
    connection = CodeRepositoryStorageConnection.objects.get(id=connection_id)
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=connection.embedding_chunk_size, chunk_overlap=connection.embedding_chunk_overlap
    )
    chunks = splitter.split_text(doc["page_content"])
    clean_chunks = []
    for i, chunk in enumerate(chunks):
        doc["metadata"]["chunk_index"] = i
        clean_chunk = {"page_content": chunk, "metadata": doc["metadata"]}
        clean_chunks.append(clean_chunk)
    print(f"[tasks.split_repository_into_chunks] Repository chunked into {len(clean_chunks)} chunk(s).")
    return clean_chunks

