from apps._services.knowledge_base.document.knowledge_base_decoder import KnowledgeBaseSystemDecoder
from apps.datasource_knowledge_base.models import DocumentKnowledgeBaseConnection


def execute_knowledge_base_query(connection_id: int, query: str, alpha: float):

    knowledge_base_connection = DocumentKnowledgeBaseConnection.objects.get(id=connection_id)

    try:
        client = KnowledgeBaseSystemDecoder().get(connection=knowledge_base_connection)
        knowledge_base_response = client.search_hybrid(query=query, alpha=alpha)
    except Exception as e:
        error = f"[knowledge_base_query_execution_handler.execute_knowledge_base_query] Error occurred while executing the knowledge base query: {str(e)}"
        return error
    return knowledge_base_response
