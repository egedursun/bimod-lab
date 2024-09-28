def validate_custom_script_retriever_tool_json(tool_usage_json: dict):
    if "parameters" not in tool_usage_json:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the
            Custom Script Content Retriever tool. Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """
    parameters = tool_usage_json.get("parameters")

    if "custom_script_reference_id" not in parameters:
        return """
            The 'custom_script_reference_id' field is missing from the 'parameters' field in the tool_usage_json. This field is
            mandatory for using the Custom Script Content Retriever tool. Please make sure you are defining the 'custom_script_reference_id'
            field in the parameters field of the tool_usage_json.
        """
    print(
        f"[custom_script_content_retriever_tool_validator.validate_custom_script_retriever_tool_json] Validation is successful.")
    return None
