from apps._services.codebase.codebase_decoder import CodeBaseDecoder
from apps.datasource_codebase.models import CodeRepositoryStorageConnection


def execute_code_base_query(connection_id: int, query: str, alpha: float):

    knowledge_base_connection = CodeRepositoryStorageConnection.objects.get(id=connection_id)
    print(f"[code_base_query_execution_handler.execute_code_base_query] Executing the code base query: {query}.")
    try:
        client = CodeBaseDecoder().get(connection=knowledge_base_connection)
        knowledge_base_response = client.search_hybrid(query=query, alpha=alpha)
    except Exception as e:
        error = f"[code_base_query_execution_handler.execute_code_base_query] Error occurred while executing the code base query: {str(e)}"
        return error
    print(f"[code_base_query_execution_handler.execute_code_base_query] Code base query executed successfully.")
    return knowledge_base_response
