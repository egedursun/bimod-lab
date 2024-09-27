from apps._services.knowledge_base.document.helpers.document_chunk_embedder import embed_document_chunks_helper


def embed_document_chunks(executor_params, chunks, path, document_id, document_uuid):
    try:
        error = embed_document_chunks_helper(
            executor_params=executor_params,
            chunks=chunks,
            path=path,
            document_id=document_id,
            document_uuid=document_uuid
        )
    except Exception as e:
        error = f"[tasks.embed_document_chunks] Error embedding the document chunks: {e}"
    return error
