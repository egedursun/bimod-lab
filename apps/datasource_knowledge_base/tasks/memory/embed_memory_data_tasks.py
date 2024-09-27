from apps._services.knowledge_base.document.helpers.document_embedder import embed_memory_helper


def embed_memory_data(executor_params, number_of_chunks):
    doc_id, doc_uuid = None, None
    try:
        doc_id, doc_uuid, error = embed_memory_helper(
            executor_params=executor_params,
            number_of_chunks=number_of_chunks
        )
    except Exception as e:
        error = f"[tasks.embed_memory_data] Error embedding the memory: {e}"
    return doc_id, doc_uuid, error
