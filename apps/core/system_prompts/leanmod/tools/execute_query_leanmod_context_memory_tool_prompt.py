#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: execute_query_intra_context_memory_tool_prompt.py
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


from apps.core.tool_calls.utils import ToolCallDescriptorNames


def build_tool_prompt__leanmod_context_memory():
    response_prompt = f"""
        ### **TOOL**: Vector Chat History (Long Term Memory) Query Execution

        - The Vector Chat History Query Execution Tool is a tool you can use to search within chat history with user,
        as this is a vector-based tool, it has an infinite capacity for you to bypass limits of 'context window'.

        - The format for dictionary you will output to use Vector Chat History Query Execution Tool is as follows:

        '''
            {{
                "tool": "{ToolCallDescriptorNames.EXECUTE_INTRA_MEMORY_QUERY}",
                "parameters": {{
                    "query": "..."
                    }}
                }}
        '''

        ---

        #### **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

        #### **INSTRUCTIONS:** The "query" will be the string you need to search in your chat history with user.

        To use, you need to provide following fields 'VERY CAREFULLY':

        - [1] The "query" field must be a string you need to search in the memory documents. This can be a question or
        keyword you would like to search within memory.

        #### **NOTE**: The system will provide you the results in the next 'assistant' message.
        This message will have a list of memories most relevant to the given query.

            - You are expected to take in this, and use it to provide answer to user's question.

    """
    return response_prompt
