

def get_orchestration_json_decode_error_log(error_logs):
    return f"""
        **SYSTEM MESSAGE:**

        - An error occurred while decoding the JSON response provided by the AI assistant. This might be
        related to the incorrect formatting of the response. Please make sure that the response is in the
        correct JSON format.

        Error Details:
        '''
        {str(error_logs)}
        '''
    """


def validate_orchestration_main_tool_json(tool_usage_json: dict):
    if not tool_usage_json:
        return """
                    The JSON is empty. Please make sure you are passing the correct JSON object to the
                    ToolDecoder class.
                """

    if not tool_usage_json.get("tool"):
        return """
                    The 'tool' field is missing from the tool_usage_json. Please make sure you are defining the tool
                    name in the tool_usage_json.
                """
    print(f"[const.validate_main_tool_json] Validation is successful.")
    return None


def get_no_orchestration_tool_found_error_log(query_name):
    return f"""
        There is no tool with the name: {query_name} in the system. Please make sure you are defining
        the correct tool name in the tool_usage_json.
    """
