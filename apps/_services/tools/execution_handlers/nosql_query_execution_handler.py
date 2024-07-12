from apps._services.nosql.nosql_decoder import InternalNoSQLClient
from apps.datasource_nosql.models import NoSQLDatabaseConnection


def execute_nosql_query(connection_id: int, query_type: str, nosql_query: str):
    nosql_response = None

    nosql_connection = NoSQLDatabaseConnection.objects.get(id=connection_id)

    client = InternalNoSQLClient().get(
        connection=nosql_connection
    )

    if query_type == "write":
        nosql_response = client.execute_write(
            query=nosql_query
        )
    elif query_type == "read":
        nosql_response = client.execute_read(
            query=nosql_query
        )

    return nosql_response
