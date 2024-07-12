from apps._services.sql.sql_decoder import InternalSQLClient
from apps.datasource_sql.models import SQLDatabaseConnection


def execute_sql_query(connection_id: int, query_type: str, sql_query: str):
    sql_response = None

    sql_connection = SQLDatabaseConnection.objects.get(id=connection_id)

    client = InternalSQLClient().get(
        connection=sql_connection
    )

    if query_type == "write":
        sql_response = client.execute_write(
            query=sql_query
        )
    elif query_type == "read":
        sql_response = client.execute_read(
            query=sql_query
        )

    return sql_response
