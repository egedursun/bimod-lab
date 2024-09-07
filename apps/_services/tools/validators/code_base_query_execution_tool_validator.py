
from apps.datasource_codebase.models import CodeRepositoryStorageConnection


def validate_code_base_query_execution_tool_json(tool_usage_json: dict):
    if "parameters" not in tool_usage_json:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the Code
            Base Query Execution tool. Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """
    parameters = tool_usage_json.get("parameters")

    if "query" not in parameters:
        return """
            The 'query' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Code Base Query Execution tool. Please make sure you are defining the 'query' field in the
            parameters field of the tool_usage_json.
        """
    if "alpha" not in parameters:
        return """
            The 'alpha' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Code Base Query Execution tool. Please make sure you are defining the 'alpha' field in the
            parameters field of the tool_usage_json.
        """

    connection = CodeRepositoryStorageConnection.objects.get(id=parameters.get("code_base_storage_connection_id"))
    if not connection:
        return f"""
            The Code Base Storage Connection with the ID: {connection.id} does not exist in the system.
            Please make sure you are passing a valid code base storage connection ID.
        """
    print(f"[code_base_query_execution_tool_validator.validate_code_base_query_execution_tool_json] Validation is successful.")
    return None
