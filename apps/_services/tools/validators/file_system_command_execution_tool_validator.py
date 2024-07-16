
"""
                {{
                    "tool": "{ToolTypeNames.FILE_SYSTEM_COMMAND_EXECUTION}",
                    "parameters": {{
                        "file_system_connection_id": "...",
                        "commands": ["...", "...", "..."]
                        }}
                    }}
"""


def validate_file_system_command_execution_tool_json(tool_usage_json: dict):
    if "parameters" not in tool_usage_json:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the File System
            Command Execution tool. Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """
    parameters = tool_usage_json.get("parameters")

    if "file_system_connection_id" not in parameters:
        return """
            The 'file_system_connection_id' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the File System Command Execution tool. Please make sure you are defining the 'file_system_connection_id' field in the
            parameters field of the tool_usage_json.
        """
    if "commands" not in parameters:
        return """
            The 'commands' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the File System Command Execution tool. Please make sure you are defining the 'commands' field in the
            parameters field of the tool_usage_json.
        """

    if not isinstance(parameters.get("commands"), list):
        return """
            The 'commands' field in the 'parameters' field of the tool_usage_json is not a list. This field should be a list of strings
            that you would like to execute on the file system. Please make sure you are defining the 'commands' field as a list of strings
            in the parameters field of the tool_usage_json.
        """

    if not all(isinstance(command, str) for command in parameters.get("commands")):
        return """
            The 'commands' field in the 'parameters' field of the tool_usage_json is not a list of strings. This field should be a list of strings
            that you would like to execute on the file system. Please make sure you are defining the 'commands' field as a list of strings
            in the parameters field of the tool_usage_json.
        """

    return None
