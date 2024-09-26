from langchain_text_splitters import RecursiveCharacterTextSplitter


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
