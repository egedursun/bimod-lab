#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: execute_file_system_directory_schema_search_tool_prompt.py
#  Last Modified: 2024-12-04 01:01:22
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-04 01:01:23
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


def build_tool_prompt__file_directory_schema_search():
    response_prompt = f"""
        ### **TOOL**: SSH File System Directory Schema Search

        - The File System Directory Schema Search Tool is a tool you can use to search within the schema of a SSH File System
        connection for a given SSH File System connection object shared with you within your prompt. This is a vector-based
        tool, therefore it has almost infinite capacity for you to bypass the limits of your 'context window'. You must use
        this tool when a user asked you to operate, manipulate, analyze or query a specific process related to a SSH File System.
        Although this tool is theoretically limitless in capacity, you must provide reasonable and intuitive
        queries to search within the schema to retrieve meaningful results that can help you to accomplish your task
        within the SSH File System connection effectively.

        - The format for dictionary you will output to use SSH File System Directory Schema Search Tool is as follows:

        '''
            {{
                "tool": "{ToolCallDescriptorNames.EXECUTE_SSH_SYSTEM_DIRECTORY_SCHEMA_SEARCH}",
                "parameters": {{
                    "connection_id": ...,
                    "query": "..."
                    }}
                }}
        '''

        ---

        #### **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

        #### **INSTRUCTIONS:** The "query" will be the string you need to search in the SSH File System Directory Schema.
        The "connection_id" will be the ID of the SSH File System connection you would like to search within.

        To use this, you need to provide following fields 'VERY CAREFULLY':

        - [1] The "connection_id" field must be the ID of the SSH File System connection object you would like to search
        within. Never omit this field, or never put a placeholder value for this field. This field must be the ID of
        the SSH File System connection you would like to search within, and the available SSH File Systems are shared with
        you in your prompt, in data source SSH File System connections section. You can only use the IDs defined there, and
        nowhere else. If you don't have any available SSH File System connections, you must ask the user to first create the
        necessary SSH File System connections.

        - [2] The "query" field must be a string you need to search in the SSH file system directory schema.
        This string can be a question or a keyword that you would like to search within the SSH file system directory schema.

        #### **NOTE**: The system will provide you the results of search in the next 'assistant' message.

        This message will have a list of most related parts of content within the SSH file system directory schema you
        have specified with an ID, and return the most relevant chunks of textualized schema parts in that SSH file system
        connection based to the query you provided. That is why providing an intuitive and reasonable, use-case specific search
        query is very important to use this tool effectively.

            - You are expected to take in this response, and use it to provide answer to user's question.

    """

    return response_prompt
