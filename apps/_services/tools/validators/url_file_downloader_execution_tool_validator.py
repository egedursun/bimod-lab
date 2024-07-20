

def validate_url_file_downloader_execution_tool_json(tool_usage_json: dict):
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

    if "url" not in parameters:
        return """
            The 'download_url' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
            for using the Media Storage Query Execution tool. Please make sure you are defining the 'download_url' field in
            the parameters field of the tool_usage_json.
        """

    return None
