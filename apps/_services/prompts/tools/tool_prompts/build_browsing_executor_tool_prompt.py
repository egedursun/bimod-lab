from apps._services.tools.const import ToolTypeNames
from config.settings import MEDIA_URL


def build_structured_tool_prompt__browsing_executor():
    response_prompt = f"""
            **TOOL**: Browsing Executor Tool

            - The Browsing Executor Tool is a tool that allows you to execute browsing operations on the web using
            the browsing datasource connections that are available for use. You can use this tool to search for
            information on the web, and click on URLs in search results to understand the contents to provide
            better answers to the users. You can use the browsing datasource connections that are available for use
            to execute these browsing operations.

            - The standardized format for the dictionary that you will output to use the Browsing Executor Tool is as
             follows:

             There are 2 different ACTIONS you can perform with the Browsing Executor Tool:

            [1] 'browser_search': This action is used to search for information on the web. You need to provide the
            'browser_connection_id', 'action', 'query', and 'page' fields in the 'parameters' field of the tool_usage_json
            to use this action. You can use this action to search for information on the web based on the query that you
            provide. The 'page' field is used to specify the page number of the search results that you would like to
            retrieve. The system will provide you with the search results based on the query that you provide.

            '''
                {{
                    "tool": "{ToolTypeNames.BROWSING}",
                    "parameters": {{
                        "browser_connection_id": "...",
                        "action": "browser_search",
                        "query": "...",
                        "page": 3
                    }}
                }}
            '''
            --- **RECOMMENDATION:** Start with the 'page' value as 1. If you need more search results, you can increase
            the 'page' value to get more search results in your latter queries.

            [2] 'click_url_in_search': This action is used to click on URLs in search results. You need to provide the
            'browser_connection_id', 'action', 'search_results', and 'click_url' fields in the 'parameters' field of the
            tool_usage_json to use this action. You can use this action to click on URLs in the search results that are
            provided to you. The 'search_results' field should be a list of search results that are provided to you, and
            the 'click_url' field should be the URL that you would like to click on.

            '''
                {{
                    "tool": "{ToolTypeNames.BROWSING}",
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
            --- **RECOMMENDATION:** The 'search_results' field should be a list of search results that are provided to you.
            You must at least include the 'url' field in each search result in the 'search_results' list. And please notice
            that each element of the 'search_results' list should be a dictionary with the 'url' field. You can include
            additional fields in the search results if you think they are necessary for the browsing operation but
            it will not be used by the system at all and be neglected. 'click_url' field should be the URL that you would
            like to click on.

            **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            **INSTRUCTIONS:** The "browser_connection_id" field should be the ID of the browsing datasource connection
            that you would like to use to execute the browsing operations. The "action" field should be the action that
            you would like to perform with the Browsing Executor Tool. The "query" field should be the query that you
            would like to search for on the web. The "page" field should be the page number of the search results that
            you would like to retrieve. The "search_results" field should be a list of search results that are provided
            to you. The "click_url" field should be the URL that you would like to click on.

            To use this tool, you need to provide the following field 'VERY CAREFULLY':

            1. For "browser_connection_id", provide the ID of the browsing datasource connection that you would like to
            use to execute the browsing operations. You can find the ID of the browsing datasource connection in the
            browsing datasource connections that are available for use.

            2. For "action", provide the action that you would like to perform with the Browsing Executor Tool. The
            action should be one of the following values: 'browser_search', 'click_url_in_search'.

            3. For "query", provide the query that you would like to search for on the web. You must provide the query
            in natural language. The system will understand the query that you provide and execute the browsing operation
            based on the query that you provide.
                - ONLY USE FOR 'browser_search' ACTION.

            4. For "page", provide the page number of the search results that you would like to retrieve. You can start
            with the 'page' value as 1. If you need more search results, you can increase the 'page' value to get more
            search results in your latter queries.
                - ONLY USE FOR 'browser_search' ACTION.

            5. For "search_results", provide a list of search results that are provided to you. You must at least include
            the 'url' field in each search result in the 'search_results' list. And please notice that each element of
            the 'search_results' list should be a dictionary with the 'url' field. You can include additional fields in
            the search results if you think they are necessary for the browsing operation but it will not be used by the
            system at all and be neglected.
                - ONLY USE FOR 'click_url_in_search' ACTION.

            6. For "click_url", provide the URL that you would like to click on. You must provide the URL in the 'click_url'
            field. The system will click on the URL that you provide in the 'click_url' field.
                - ONLY USE FOR 'click_url_in_search' ACTION.

            ---

            **IMPORTANT NOTES:**

            **NOTE**: The system will provide you with the results in the next 'assistant' message. This message will
            have the output of the browsing operation that you have executed. The system will provide you with the
            results based on the browsing operation that you have executed. Then, you will be free to decide another
            action to take within the browsing context, OR if you think you have enough information, you can end the
            browsing operation by closing the browser and then answering the user's question by using your own
            words based on the browsing operation that you have executed.

            **ABOUT YOU PROVIDING LINKS:**
            - If you need to provide a direct link to the user for reaching the files, here is the base
                URL you need to 'DIRECTLY' append the file path to provide an absolute HTTP reference to the file:
                - {MEDIA_URL}
            - **NEVER, EVER:** provide a 'relative' path to the files. Always provide the 'absolute' path by
            appending the file path to the base URL.

        """
    return response_prompt
