from apps.datasource_nosql.models import NoSQLDatabaseConnection


def validate_nosql_query_execution_tool_json(tool_usage_json: dict):
    if "parameters" not in tool_usage_json:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the NoSQL
            Query Execution tool. Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """
    parameters = tool_usage_json.get("parameters")

    if "query" not in parameters:
        return """
            The 'query' field is missing from the 'parameters' field in the tool_usage_json. This field is
            mandatory for using the NoSQL Query Execution tool. Please make sure you are defining the 'query' field
            in the parameters field of the tool_usage_json.
        """
    if "database_connection_id" not in parameters:
        return """
            The 'database_connection_id' field is missing from the 'parameters' field in the tool_usage_json. This
            field is mandatory for using the NoSQL Query Execution tool. Please make sure you are defining the
            'database_connection_id' field in the parameters field of the tool_usage_json.
        """
    if "type" not in parameters:
        return """
            The 'type' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the NoSQL Query Execution tool. This must either be 'read' or 'write' based on the type of query you
            are executing. Please make sure you are defining the 'type' field in the parameters field of the
            tool_usage_json.
        """
    query_type = parameters.get("type")
    if query_type not in ["read", "write"]:
        return """
            The 'type' field in the 'parameters' field of the tool_usage_json must either be 'read' or 'write'. This
            field is mandatory for using the NoSQL Query Execution tool. Please make sure you are defining the 'type'
            field in the parameters field of the tool_usage_json.
        """

    connection = NoSQLDatabaseConnection.objects.get(id=parameters.get("database_connection_id"))
    if not connection:
        return f"""
            The NoSQL Database Connection with the ID: {connection.id} does not exist in the system.
            Please make sure you are passing a valid database connection ID.
        """
    return None
