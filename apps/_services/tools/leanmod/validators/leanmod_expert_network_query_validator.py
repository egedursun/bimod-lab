def validate_expert_network_query_tool_json(tool_usage_json):
    if "parameters" not in tool_usage_json:
        return """
            The 'parameters' is missing from tool_usage_json. This field is mandatory to use Expert Network Query
            Execution tool.
        """
    parameters = tool_usage_json.get("parameters")

    if "assistant_id" not in parameters:
        return """
            The 'alpha' field is missing from 'parameters' field in tool_usage_json. This field is mandatory for
            using Expert Network Query Execution tool.
        """

    if "query" not in parameters:
        return """
            The 'query' field is missing from 'parameters' field in tool_usage_json. This field is mandatory for
            using Expert Network Query Execution tool.
        """

    if not isinstance(parameters.get("image_urls"), list) and parameters.get("image_urls") is not None:
        return """
            The 'image_urls' field must be a list of URLs of images.
        """

    if not isinstance(parameters.get("file_urls"), list) and parameters.get("file_urls") is not None:
        return """
            The 'file_urls' field must be a list of URLs of files.
        """

    print(
        f"[leanmod_expert_network_query_validator.validate_expert_network_query_tool_json] Validation is successful.")
    return None
