

class ToolTypeNames:
    ##############################
    SQL_QUERY_EXECUTION = 'SQL Query Execution'
    NOSQL_QUERY_EXECUTION = 'NoSQL Query Execution'
    KNOWLEDGE_BASE_QUERY_EXECUTION = 'Knowledge Base Query Execution'
    CODE_BASE_QUERY_EXECUTION = 'Code Base Query Execution'
    VECTOR_CHAT_HISTORY_QUERY_EXECUTION = 'Vector Chat History Query Execution'
    FILE_SYSTEM_COMMAND_EXECUTION = 'File System Command Execution'
    MEDIA_STORAGE_QUERY_EXECUTION = 'Media Storage Query Execution'
    BROWSING = 'Browsing'
    URL_FILE_UPLOADER = 'URL File Uploader'
    URL_FILE_DOWNLOADER = 'URL File Downloader'
    PREDICTION_WITH_ML_MODEL = 'Prediction with ML Model'
    CODE_INTERPRETER = 'Code Interpreter'
    CUSTOM_FUNCTION_EXECUTOR = 'Custom Function Executor'
    CUSTOM_API_EXECUTOR = 'Custom API Executor'
    CUSTOM_SCRIPT_CONTENT_RETRIEVAL = 'Custom Script Content Retrieval'
    IMAGE_GENERATION = 'Image Generation'
    IMAGE_MODIFICATION = 'Image Modification'
    IMAGE_VARIATION = 'Image Variation'
    AUDIO_PROCESSING = 'Audio Processing'
    ##############################
    EXPERT_NETWORK_QUERY_CALL = 'Expert Network Query Call'
    ##############################
    ORCHESTRATION_WORKER_ASSISTANT_CALL = 'Orchestration Worker Assistant Call'
    ##############################


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
