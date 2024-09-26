from apps._services.codebase.helpers.repository_embedder import embed_repository_helper


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
