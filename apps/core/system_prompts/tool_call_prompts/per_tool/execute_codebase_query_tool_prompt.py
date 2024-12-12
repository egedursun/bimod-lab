#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: build_code_base_query_execution_tool_prompt.py
#  Last Modified: 2024-10-05 02:26:00
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:35
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


from apps.core.tool_calls.utils import (
    ToolCallDescriptorNames
)


def build_tool_prompt__execute_codebase_query():
    response_prompt = f"""

            ### **TOOL**: Code Base Search Query Execution

            - The Code Base Query Execution Tool is a tool you can use to search within the connected code base
            repositories of user to provide more accurate responses to their questions. You can try to reach any of the
            specified code bases defined within the "Code Base Storage Connections" section.

            - The format for the dictionary you will output to use Code Base Query Execution Tool is as follows:

            '''
                {{
                    "tool": "{ToolCallDescriptorNames.EXECUTE_CODE_BASE_QUERY}",
                    "parameters": {{
                        "connection_id": "...",
                        "repository_uri": "...", (optional)
                        "query": "...",
                        }}
                    }}
            '''

            ---

            #### **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            #### **INSTRUCTIONS:** The "connection_id" will be the ID of Code Base Storage Connection
            you need to execute your query, and "query" will be the string you need to search within the code base
            storage repos. The "repository_uri" is optional, and if you provide it, the search will be limited to
            that repository only. If you do not provide it, the search will be conducted across all repositories
            in the storage connection you have specified.

            To use this, you need to provide following fields 'VERY CAREFULLY':

            - [1] The "query" field should be a string that you would like to search within the code base storage repositories.
            This string can be a question or a keyword that you would like to search within the repositories.

            - [2] The "connection_id" field should be the ID of the Code Base Storage Connection you would like to use
            to search within the repositories. You can find the ID of the Code Base Storage Connection by checking the
            Code Base Storage Connections that are available for you.

            - [3] The "repository_uri" field is optional, and if you provide it, the search will be limited to that
            repository only. If you do not provide it, the search will be conducted across all repositories in the storage
            connection you have specified.

            #### **NOTE**: The system will provide you the results of search in the next 'assistant' message.
            This message will have a list of repository contents that are most relevant to query you have provided.
            You are expected to take in this response, and use it to provide a more accurate and informative answer
            to user's questions.

            ---

        """

    return response_prompt
