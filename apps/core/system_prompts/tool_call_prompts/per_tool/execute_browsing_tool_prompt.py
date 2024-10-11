#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: build_browsing_executor_tool_prompt.py
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
#   For permission inquiries, please contact: admin@br6.in.
#


from apps.core.tool_calls.utils import ToolCallDescriptorNames
from config.settings import MEDIA_URL


def build_tool_prompt__browsing():
    response_prompt = f"""
            ### **TOOL**: Browsing Executor Tool

            - The Browsing Executor Tool is a tool allows you to execute browsing operations on web using browsing
            datasource connections available for you to use. You can use this to search for information online, and
            click on URLs in search results to understand contents to provide better answers to the users. You can
            use browsing datasource connections available for use to execute these browsing operations.

            - The format for the dict you will output to use Browsing Executor Tool is as follows:

            '''
                {{
                    "tool": "{ToolCallDescriptorNames.EXECUTE_BROWSING}",
                    "parameters": {{
                        "browser_connection_id": "...",
                        "action": "browser_search",
                        "query": "...",
                        "page": 3
                    }}
                }}
            '''

            There are 2 different ACTIONS you can perform with Browsing Executor Tool:

                - [1] 'browser_search': This action is used to search for information online. You need to provide
                'browser_connection_id', 'action', 'query', and 'page' fields in 'parameters' field of tool_usage_json
                to use this action. You can use this to search for information online based on a query you provide.
                The 'page' field is used to specify page number of search results you would like to retrieve. The
                system will provide you the search results based on your query.

                    - **RECOMMENDATION:** Start with the 'page' value of "1". If you need more results, you can increase
                    the 'page' value to get more results in latter queries.

                - [2] 'click_url_in_search': This action is used to click on URLs in search results. You need to
                provide 'browser_connection_id', 'action', 'search_results', and 'click_url' fields in 'parameters'
                field of the tool_usage_json to use this action. You can use this to click on URLs in search results
                you received. The 'search_results' field must be a list of results, and the 'click_url' field must
                be the URL you want to click on.

                    - **RECOMMENDATION:** The 'search_results' field should be a list of search results that are
                    provided to you. You must at least include the 'url' field in each search result in the
                    'search_results' list. And please notice that each element of the 'search_results' list should
                    be a dictionary with the 'url' field. You can include additional fields in the search results
                    if you think they are necessary for the browsing operation but it will not be used by the system
                    at all and be neglected. 'click_url' field should be the URL that you would like to click on.

                    '''
                        {{
                            "tool": "{ToolCallDescriptorNames.EXECUTE_BROWSING}",
                            "parameters": {{
                                "browser_connection_id": "...",
                                "action": "click_url_in_search",
                                "search_results": [
                                    {{
                                        "url": "..."
                                    }},
                                    {{
                                        "url": "..."
                                    }}
                                    ...
                                ],
                                "click_url": "..."
                            }}
                        }}
                    '''

            ---

            #### **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            #### **INSTRUCTIONS:** The "browser_connection_id" should be the ID of the browsing datasource connection
            you need to use to execute browsing operations. The "action" should be the action you need to perform.
            The "query" should be the query that you need to search for online. The "page" should be the page number
            of search results that you want to retrieve. The "search_results" must be a list of results that are
            provided to you. The "click_url" must be the URL you want to click on.

            To use this tool, you need to provide the following field 'VERY CAREFULLY':

            - [1] For "browser_connection_id", provide the ID of the browsing datasource connection you need to use to
            execute browsing operations. You can find ID of the browsing datasource connection in browsing datasource
            connections available for your use.

            - [2] For "action", provide the action you need to perform with Browsing Executor Tool. The action must be
            one of the following values: 'browser_search', 'click_url_in_search'.

            - [3] For "query", provide the query you want to search for online. You must provide the query in natural
            language. The system will understand the query you provided and execute browsing operation. (ONLY USE THIS
            FIELD FOR 'browser_search' ACTION.)

            - [4] For "page", provide the page number of search results you want to retrieve. You can start with 'page'
             value as 1. If you need more results, you can increase 'page' value to get more results in your latter
             queries. (ONLY USE THIS FIELD FOR 'browser_search' ACTION.)

            - [5] For "search_results", provide a list of search results that are provided. You must at least include
            the 'url' field in each search result in 'search_results' list. And notice that each element of
            'search_results' list must be a dictionary with 'url' field. You can include more fields in search results
            if you think they are necessary for browsing operation but it will not be used by the system and be
            neglected. (ONLY USE THIS FIELD FOR 'click_url_in_search' ACTION.)

            - [6] For "click_url", provide URL you need to click on. You must provide URL in the 'click_url'
            field. The system will click on URL you provided in this field. (ONLY USE THIS FIELD FOR
            'click_url_in_search' ACTION.)

            ---

            #### **IMPORTANT NOTES:**

            #### **NOTE**: The system will provide you the results in next 'assistant' message. This message will
            have output of the operation you executed. The system will provide you with the results based on the
            operation. Then, you will be free to decide on another action to take within the browsing context, [OR] if
            you think you have enough data, you can end the browsing operations by closing the browser and then
            answering user's question with your own words.

            #### **ABOUT PROVIDING URLS & LINKS:**

                - If you need to provide a direct link to user for reaching files, here is the base URL you need to
                'DIRECTLY' append the file path to provide an absolute HTTP URL to file:
                    - {MEDIA_URL}

                - **NEVER, EVER:** provide a 'relative' path to files. Always provide 'absolute' path by appending
                the file path to the base URL.

            ---

        """
    return response_prompt
