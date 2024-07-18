

def validate_media_storage_query_execution_tool_json(tool_usage_json: dict):
    if "parameters" not in tool_usage_json:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the SQL Query
            Execution tool. Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """
    parameters = tool_usage_json.get("parameters")

    if "media_storage_connection_id" not in parameters:
        return """
            The 'media_storage_connection_id' field is missing from the 'parameters' field in the tool_usage_json. This
            field is mandatory for using the Media Storage Query Execution tool. Please make sure you are defining the
            'media_storage_connection_id' field in the parameters field of the tool_usage_json.
        """

    if "query" not in parameters:
        return """
            The 'query' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Media Storage Query Execution tool. Please make sure you are defining the 'query' field in the
            parameters field of the tool_usage_json.
        """

    if "type" not in parameters:
        return """
            The 'type' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Media Storage Query Execution tool. Please make sure you are defining the 'type' field in the
            parameters field of the tool_usage_json. The available types are "file_interpretation" and
            "image_interpretation".
        """

    if parameters.get("type") not in ["file_interpretation", "image_interpretation"]:
        return """
            The 'type' field in the 'parameters' field of the tool_usage_json must either be 'file_interpretation' or
            'image_interpretation'. This field is mandatory for using the Media Storage Query Execution tool. Please make
            sure you are defining the 'type' field in the parameters field of the tool_usage_json.
        """

    if "file_paths" not in parameters:
        return """
            The 'file_paths' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
            for using the Media Storage Query Execution tool. Please make sure you are defining the 'file_paths' field in
            the parameters field of the tool_usage_json.
        """

    if not isinstance(parameters.get("file_paths"), list):
        return """
            The 'file_paths' field in the 'parameters' field of the tool_usage_json must be a list. This field is
            mandatory for using the Media Storage Query Execution tool. Please make sure you are defining the 'file_paths'
            field in the parameters field of the tool_usage_json.
        """

    return None
