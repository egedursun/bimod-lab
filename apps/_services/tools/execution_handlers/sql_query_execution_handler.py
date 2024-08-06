from apps._services.sql.sql_decoder import InternalSQLClient
from apps.datasource_sql.models import SQLDatabaseConnection


def execute_sql_query(connection_id: int, query_type: str, sql_query: str):
    sql_response = None
    sql_connection = SQLDatabaseConnection.objects.get(id=connection_id)
    print(f"[sql_query_execution_handler.execute_sql_query] Executing the SQL query: {sql_query}.")
    try:
        client = InternalSQLClient().get(
            connection=sql_connection
        )
        if query_type == "write":
            print(f"[sql_query_execution_handler.execute_sql_query] Executing the SQL write query: {sql_query}.")
            sql_response = client.execute_write(query=sql_query)
        elif query_type == "read":
            print(f"[sql_query_execution_handler.execute_sql_query] Executing the SQL read query: {sql_query}.")
            sql_response = client.execute_read(query=sql_query)
    except Exception as e:
        error = f"[sql_query_execution_handler.execute_sql_query] Error occurred while executing the SQL query: {str(e)}"
        return error
    print(f"[sql_query_execution_handler.execute_sql_query] SQL query executed successfully.")
    return sql_response
