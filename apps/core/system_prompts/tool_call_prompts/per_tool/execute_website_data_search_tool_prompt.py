#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: execute_website_data_search_tool_prompt.py
#  Last Modified: 2024-12-09 01:31:31
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-09 01:31:32
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


def build_tool_prompt__website_data_search():
    response_prompt = f"""
        ### **TOOL**: Website Storage Item Data Search

        - The Website Storage Item Data Search Tool is a tool you can use to search within the content of a Website
        for a given Website Storage connection object shared with you within your prompt. This is a vector-based tool,
        therefore it has almost infinite capacity for you to bypass the limits of your 'context window'. You must use
        this tool when a user asked you to analyze or query a specific process related to a website that is specified
        within a Website Storage, which is a wrapper for embedding and indexing the content of multiple websites.
        Although this tool is theoretically limitless in capacity, you must provide reasonable and intuitive
        queries to search within the website data to retrieve meaningful results that can help you to accomplish your task
        within the context and user query's scope effectively.

        - The format for dictionary you will output to use Website Storage Item Data Search Tool is as follows:

        '''
            {{
                "tool": "{ToolCallDescriptorNames.EXECUTE_WEBSITE_DATA_SEARCH_QUERY}",
                "parameters": {{
                    "connection_id": ...,
                    "website_url": "...", (optional)
                    "query": "..."
                    }}
                }}
        '''

        ---

        #### **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

        #### **INSTRUCTIONS:** The "query" will be the string you need to search in the SQL Database Schema.
        The "connection_id" will be the ID of the SQL Database connection you would like to search within.

        To use this, you need to provide following fields 'VERY CAREFULLY':

        - [1] The "connection_id" field must be the ID of the Website Storage Connection object you would like to search
        within. Never omit this field, or never put a placeholder value for this field. This field must be the ID of
        the Website Storage connection you would like to search a website located within, and the available Website Storages
        are shared with you in your prompt, in data source Website Storage connections section. You can only use the IDs
        defined there, and nowhere else. If you don't have any available Website Storage connections, you must ask the
        user to first create the necessary Website Storage connections.

        - [2] The "website_url" field must be the URL of the website you would like to search within. This field must be
        one of the URLs of the websites located within the Website Storage connection you have specified with an ID. If
        you leave this field empty, the system will search within all the websites located within the Website Storage
        connection you have specified with an ID.

        - [3] The "query" field must be a string you need to search in the content of the website located within the
        Website Storage connection. This string can be a question or a keyword that you would like to search within the
        content of the website.

        #### **NOTE**: The system will provide you the results of search in the next 'assistant' message.

        This message will have a list of most related parts of content within the Website Storage connection you have specified
        with an ID, and return the most relevant chunks of textualized schema parts in that Website Storage connection
        based to the query you provided. That is why providing an intuitive and reasonable, use-case specific search
        query is very important to use this tool effectively.

            - You are expected to take in this response, and use it to provide answer to user's question.

    """

    return response_prompt
