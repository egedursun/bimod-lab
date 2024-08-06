from apps._services.knowledge_base.memory.memory_executor import MemoryExecutor
from apps.datasource_knowledge_base.models import ContextHistoryKnowledgeBaseConnection


def execute_memory_query(connection_id: int, query: str, alpha: float):

    memory_connection = ContextHistoryKnowledgeBaseConnection.objects.get(id=connection_id)
    print(f"[memory_query_execution_handler.execute_memory_query] Executing the memory query: {query}.")
    try:
        c = MemoryExecutor(connection=memory_connection)
        memory_response = c.search_hybrid(query=query, alpha=alpha)
    except Exception as e:
        error = f"[memory_query_execution_handler.execute_memory_query] Error occurred while executing the memory query: {str(e)}"
        return error
    print(f"[memory_query_execution_handler.execute_memory_query] Memory query executed successfully.")
    return memory_response
