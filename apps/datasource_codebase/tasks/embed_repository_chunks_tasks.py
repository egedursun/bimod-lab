from apps._services.codebase.helpers.repository_chunk_embedder import embed_repository_chunks_helper


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
