

def validate_code_interpreter_execution_tool_json(tool_usage_json: dict):
    if "parameters" not in tool_usage_json:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the Code
            Interpreter Execution tool. Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """
    parameters = tool_usage_json.get("parameters")

    if "query" not in parameters:
        return """
            The 'query' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Code Interpreter Execution tool. Please make sure you are defining the 'query' field in the parameters
            field of the tool_usage_json.
        """

    if "file_paths" not in parameters:
        return """
            The 'file_paths' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
            for using the Code Interpreter Execution tool. Please make sure you are defining the 'file_paths' field in the
            parameters field of the tool_usage_json.
        """

    if not isinstance(parameters.get("file_paths"), list):
        return """
            The 'file_paths' field in the 'parameters' field of the tool_usage_json must be a list. This field is
            mandatory for using the Code Interpreter Execution tool. Please make sure you are defining the 'file_paths' field in
            the parameters field of the tool_usage_json.
        """

    return None
