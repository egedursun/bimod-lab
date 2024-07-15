from apps._services.knowledge_base.document.knowledge_base_decoder import KnowledgeBaseSystemDecoder
from apps.datasource_knowledge_base.models import DocumentKnowledgeBaseConnection


def execute_knowledge_base_query(connection_id: int, query: str, alpha: float):

    knowledge_base_connection = DocumentKnowledgeBaseConnection.objects.get(id=connection_id)

    client = KnowledgeBaseSystemDecoder().get(
        connection=knowledge_base_connection
    )

    knowledge_base_response = client.search_hybrid(
        query=query,
        alpha=alpha
    )

    return knowledge_base_response
