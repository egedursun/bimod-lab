from celery import shared_task


@shared_task
def index_memory_helper(connection_id, message_text):
    from apps.datasource_knowledge_base.models import ContextHistoryKnowledgeBaseConnection
    from apps._services.knowledge_base.memory.memory_executor import MemoryExecutor
    from apps.datasource_knowledge_base.tasks import chunk_memory

    output = {"status": True, "error": None}
    connection = ContextHistoryKnowledgeBaseConnection.objects.get(id=connection_id)
    executor = MemoryExecutor(connection=connection)
    try:
        print("[tasks.index_memory_helper] Indexing memory..")
        # Chunk the message
        chunks, error = chunk_memory(message_text=message_text)
        if error or not chunks:
            print(f"[tasks.index_memory_helper] Error chunking the chat history memory: {error}")
            output = {"status": False, "error": error}
            return output

        # Embed the memory doc
        number_of_chunks = len(chunks)
        doc_id, doc_uuid, error = executor.embed_memory(number_of_chunks=number_of_chunks)
        if error or not doc_id or not doc_uuid:
            print(f"[tasks.index_memory_helper] Error embedding the memory: {error}")
            output = {"status": False, "error": error}
            return output

        # Embed the memory chunks
        error = executor.embed_memory_chunks(chunks=chunks, memory_id=doc_id, memory_uuid=doc_uuid)
        if error:
            print(f"[tasks.index_memory_helper] Error embedding the memory chunks: {error}")
            output = {"status": False, "error": error}
            return output
        print("[tasks.index_memory_helper] Memory indexed successfully..")
    except Exception as e:
        output = {"status": False, "error": str(e)}
    return output
