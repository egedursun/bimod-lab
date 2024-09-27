from langchain_text_splitters import RecursiveCharacterTextSplitter

from apps.datasource_knowledge_base.utils import MEMORY_DEFAULT_CHUNK_SIZE, MEMORY_DEFAULT_CHUNK_OVERLAP


def chunk_memory(message_text: str):
    chunks, error = [], None
    # Split the message into chunks
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=MEMORY_DEFAULT_CHUNK_SIZE,
        chunk_overlap=MEMORY_DEFAULT_CHUNK_OVERLAP
    )
    chunks = splitter.split_text(message_text)
    if chunks:
        print(f"[tasks.index_document_helper] Message chunked into {len(chunks)} chunk(s).")
    else:
        error = "[tasks.index_document_helper] Error chunking the message."
    return chunks, error
