

def validate_context_history_query_execution_tool_json(tool_usage_json: dict):
    if "parameters" not in tool_usage_json:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the Context
            History Query Execution tool. Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """
    parameters = tool_usage_json.get("parameters")

    if "query" not in parameters:
        return """
            The 'query' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Context History Query Execution tool. Please make sure you are defining the 'query' field in the
            parameters field of the tool_usage_json.
        """
    if "alpha" not in parameters:
        return """
            The 'alpha' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Context History Query Execution tool. Please make sure you are defining the 'alpha' field in the
            parameters field of the tool_usage_json.
        """
    return None
