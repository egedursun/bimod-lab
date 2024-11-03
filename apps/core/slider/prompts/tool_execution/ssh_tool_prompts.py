#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: ssh_tool_prompts.py
#  Last Modified: 2024-10-17 16:15:05
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-02 21:31:30
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from apps.core.tool_calls.utils import ToolCallDescriptorNames


def build_slider_tool_prompt__execute_ssh_file_system_command():
    response_prompt = f"""
            ### **TOOL**: File System Command Execution

            - The File System Command Execution Tool is a tool you can use to execute commands on file system
            of servers. You can use this to execute commands on file systems, retrieve file system info, and retrieve
            the schema of file systems. You can use this to retrieve info about files, directories, and other file
            system-related info; as well as execute commands on file systems to update, delete, or create files and
            directories, or develop and run scripts.

            - The format for the dictionary you will output to use File System Command Execution Tool is as follows:

            '''
                {{
                    "tool": "{ToolCallDescriptorNames.EXECUTE_SSH_SYSTEM_QUERY}",
                    "parameters": {{
                        "file_system_connection_id": "...",
                        "commands": ["...", "...", "..."]
                    }}
                }}
            '''

            ---

            #### **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            #### **INSTRUCTIONS:** The "file_system_connection_id" will be the ID of File System Connection that
            you need to execute your commands on, and "commands" will be a list of strings you need to execute on file
            system. You can provide multiple commands in list to execute them sequentially on file system. As you
            can see, "commands" is a list of strings, so you can provide multiple commands in list to execute them
            sequentially on file system.

            To use this, you need to provide the following fields 'VERY CAREFULLY':

            - [1] The "commands" field must be a list of strings you need to execute on file system. These strings
            can be commands you need to execute on file system. You can provide multiple commands in list to execute
            them sequentially on file system.

            ---

            - **NOTE**: The system will provide you the results of the commands executed in next 'assistant' message.
            This message will have the output of commands executed on file system. You can use this output to
            retrieve the info you need to provide an answer to user. You can run the tool again to execute more
            commands on file system if you think it is necessary. At the end, you are expected to take in this
            responses, and use it to provide an answer to user's question.

            ---

        """
    return response_prompt
