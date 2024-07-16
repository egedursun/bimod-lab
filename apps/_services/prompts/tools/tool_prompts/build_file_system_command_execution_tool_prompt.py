from apps._services.tools.const import ToolTypeNames


def build_structured_tool_prompt__file_system_command_execution():

    response_prompt = f"""
            **TOOL**: File System Command Execution

            - The File System Command Execution Tool is a tool you can use to execute commands on the file system
            of the server. You can use this tool to execute commands on the file system, retrieve file system
            information, and retrieve the schema of the file system. You can use this to retrieve information
            about files, directories, and other file system-related information; as well as execute commands
            on the file system to update, delete, or create files and directories, or develop and run scripts.

            - The standardized format for the dictionary that you will output to use the Knowledge Base Query Execution
            Tool is as follows:

            '''
                {{
                    "tool": "{ToolTypeNames.FILE_SYSTEM_COMMAND_EXECUTION}",
                    "parameters": {{
                        "file_system_connection_id": "...",
                        "commands": ["...", "...", "..."]
                    }}
                }}
            '''

            **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            **INSTRUCTIONS:** The "file_system_connection_id" will be the ID of the File System Connection that
            you would like to execute your commands on, and the "commands" will be a list of strings that you would
            like to execute on the file system. You can provide multiple commands in the list to execute them
            sequentially on the file system. As you can see, "commands" is a list of strings, so you can provide
            multiple commands in the list to execute them sequentially on the file system.

            To use this tool, you need to provide the following field 'VERY CAREFULLY':

            1. The "commands" field should be a list of strings that you would like to execute on the file system.
            These strings can be commands that you would like to execute on the file system. You can provide multiple
            commands in the list to execute them sequentially on the file system.

            **NOTE**: The system will provide you with the results of the commands executed in the next 'assistant' message.
            This message will have the output of the commands executed on the file system. The output will be the
            standard output of the commands executed on the file system. You can use this output to retrieve the
            information you need to provide an answer to the user. You can run the tool again to execute more
            commands on the file system if you think it is necessary.

            - At the end, you are expected to take in this responses, and use it to provide an answer to the user's
            question.

        """

    return response_prompt
