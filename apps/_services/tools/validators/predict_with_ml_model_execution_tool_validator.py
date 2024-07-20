

def validate_predict_with_ml_model_execution_tool_json(tool_usage_json: dict):
    if "parameters" not in tool_usage_json:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the SQL Query
            Execution tool. Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """
    parameters = tool_usage_json.get("parameters")

    if "ml_base_connection_id" not in parameters:
        return """
            The 'ml_base_connection_id' field is missing from the 'parameters' field in the tool_usage_json. This
            field is mandatory for using the Prediction with ML Model tool. Please make sure you are defining the
            'ml_base_connection_id' field in the parameters field of the tool_usage_json.
        """

    if "model_path" not in parameters:
        return """
            The 'model_path' field is missing from the 'parameters' field in the tool_usage_json. This field is
            mandatory for using the Prediction with ML Model tool. Please make sure you are defining the 'model_path'
            field in the parameters field of the tool_usage_json.
        """

    if "input_data_paths" not in parameters:
        return """
            The 'input_data_paths' field is missing from the 'parameters' field in the tool_usage_json. This field is
            mandatory for using the Prediction with ML Model tool. Please make sure you are defining the 'input_data_paths'
            field in the parameters field of the tool_usage_json.
        """

    if not isinstance(parameters.get("input_data_paths"), list):
        return """
            The 'input_data_paths' field in the 'parameters' field of the tool_usage_json must be a list. This field is
            mandatory for using the Prediction with ML Model tool. Please make sure you are defining the 'input_data_paths'
            field in the parameters field of the tool_usage_json.
        """

    if "query" not in parameters:
        return """
            The 'query' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Prediction with ML Model tool. Please make sure you are defining the 'query' field in the
            parameters field of the tool_usage_json.
        """

    return None
