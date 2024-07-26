

def validate_custom_function_execution_tool_json(tool_usage_json: dict):
    if "parameters" not in tool_usage_json:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the SQL Query
            Execution tool. Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """
    parameters = tool_usage_json.get("parameters")

    if "custom_function_reference_id" not in parameters:
        return """
            The 'custom_function_reference_id' field is missing from the 'parameters' field in the tool_usage_json. This field is
            mandatory for using the Custom Function Execution tool. Please make sure you are defining the 'custom_function_reference_id'
            field in the parameters field of the tool_usage_json.
        """

    if "input_data" not in parameters:
        return """
            The 'input_data' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
            for using the Custom Function Execution tool. Please make sure you are defining the 'input_data' field in the
            parameters field of the tool_usage_json.
        """

    if not isinstance(parameters.get("input_data"), dict):
        return """
            The 'input_data' field in the 'parameters' field of the tool_usage_json must be a dictionary. This field is
            mandatory for using the Custom Function Execution tool. Please make sure you are defining the 'input_data'
            field in the parameters field of the tool_usage_json.
        """

    return None
