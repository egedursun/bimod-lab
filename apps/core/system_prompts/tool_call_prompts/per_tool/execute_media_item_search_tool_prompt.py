#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: execute_media_item_search_tool_prompt.py
#  Last Modified: 2024-12-01 22:49:56
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-01 22:49:57
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


def build_tool_prompt__media_item_search():
    response_prompt = f"""
        ### **TOOL**: Media Item Search Tool

        - The Media Item Search Tool is a tool you can use to search within the media items for a given media storage
        shared with you within your prompt. This is a vector-based tool, therefore it has almost infinite capacity for
        you to bypass the limits of your 'context window'. You must use this tool when a user asked you to operate, analyze
        or query a specific media item in a media storage shared with you.

        - The format for dictionary you will output to use Media Item Search Tool is as follows:

        '''
            {{
                "tool": "{ToolCallDescriptorNames.EXECUTE_MEDIA_ITEM_SEARCH_QUERY}",
                "parameters": {{
                    "connection_id": ...,
                    "query": "..."
                    }}
                }}
        '''

        ---

        #### **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

        #### **INSTRUCTIONS:** The "query" will be the string you need to search in the storage files. The "connection_id"
        will be the ID of the media storage connection you would like to search within.

        To use this, you need to provide following fields 'VERY CAREFULLY':

        - [1] The "connection_id" field must be the ID of the media storage connection you would like to search
        within. Never omit this field, or never put a placeholder value for this field. This field must be the ID of
        the media storage connection you would like to search within, and the available media storages are shared with
        you in your prompt, in data source media storages section. You can only use the IDs defined there, and nowhere
        else. If you don't have any available media storage connections, you must ask the user to provide you
        with the necessary media storage connections.

        - [2] The "query" field must be a string you need to search in the storage files.
        This string can be a question or a keyword that you would like to search within the media storage.

        #### **NOTE**: The system will provide you the results of search in the next 'assistant' message.
        This message will have a list of media items within the media storage you have specified with an ID, and return the
        most relevant media items in that storage based to the query you provided.

            - You are expected to take in this response, and use it to provide answer to user's question.

    """
    return response_prompt
