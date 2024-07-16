from apps._services.knowledge_base.memory.memory_executor import MemoryExecutor
from apps.datasource_knowledge_base.models import ContextHistoryKnowledgeBaseConnection


def execute_memory_query(connection_id: int, query: str, alpha: float):

    memory_connection = ContextHistoryKnowledgeBaseConnection.objects.get(id=connection_id)

    c = MemoryExecutor(
        connection=memory_connection
    )
    memory_response = c.search_hybrid(
        query=query,
        alpha=alpha
    )

    return memory_response
