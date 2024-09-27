from apps._services.knowledge_base.document.helpers.document_chunk_embedder import embed_memory_chunks_helper


def embed_memory_chunks(executor_params, chunks, memory_id, memory_uuid):
    try:
        error = embed_memory_chunks_helper(
            executor_params=executor_params,
            chunks=chunks,
            memory_id=memory_id,
            memory_uuid=memory_uuid
        )
    except Exception as e:
        error = f"[tasks.embed_memory_chunks] Error embedding the memory chunks: {e}"
    return error
