def get_no_knowledge_base_connection_error_log(assistant_name, chat_name):
    return f"""
        The Context History Knowledge Base Connection for the chat: {chat_name} and assistant: {assistant_name}
        does not exist in the system. Please make sure you have the connection setup in the system.
    """


def get_no_tool_found_error_log(query_name):
    return f"""
        There is no tool with the name: {query_name} in the system. Please make sure you are defining
        the correct tool name in the tool_usage_json.
    """
