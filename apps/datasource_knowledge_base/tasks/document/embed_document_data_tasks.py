from apps._services.knowledge_base.document.helpers.document_embedder import embed_document_helper


def embed_document_data(executor_params, document, path, number_of_chunks):
    doc_id, doc_uuid = None, None
    try:
        doc_id, doc_uuid, error = embed_document_helper(
            executor_params=executor_params,
            document=document,
            path=path,
            number_of_chunks=number_of_chunks
        )
    except Exception as e:
        error = f"[tasks.embed_document_data] Error embedding the document: {e}"
    return doc_id, doc_uuid, error
