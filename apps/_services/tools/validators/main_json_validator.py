

def validate_main_tool_json(tool_usage_json: dict):
    ##################################################
    # Check if the JSON is empty
    if not tool_usage_json:
        return """
                    The JSON is empty. Please make sure you are passing the correct JSON object to the
                    ToolDecoder class.
                """
    ##################################################

    ##################################################
    # Check if the tool field is missing
    if not tool_usage_json.get("tool"):
        return """
                    The 'tool' field is missing from the tool_usage_json. Please make sure you are defining the tool
                    name in the tool_usage_json.
                """
    ##################################################

    return None
