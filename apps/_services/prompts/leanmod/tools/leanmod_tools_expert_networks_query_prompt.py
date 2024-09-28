from apps._services.tools.utils import ToolTypeNames


def build_structured_tool_prompt__expert_network_query_execution_leanmod():
    response_prompt = f"""
                TOOL: Expert Network Query Call

                - This allows consulting to expert networks. If data is not enough to respond, you can check network
                descriptions + instructions of assistants to see if they can answer.

                - The format of dict to use:

                '''
                    {{
                        "tool": "{ToolTypeNames.EXPERT_NETWORK_QUERY_CALL}",
                        "parameters": {{
                            "assistant_id": "...",
                            "query": "...",
                            "image_urls": ["..."],
                            "file_urls": ["..."]
                        }}
                    }}
                '''

                *INSTRUCTIONS*

                - "assistant_id" is ID of assistant you want to consult. Find ID of assistant by checking
                 networks/assistants you have access.
                - "query" is question/request you want to ask.
                - "image_urls" is list of URLs of images to provide to expert.
                - "file_urls" is list of URLs of files to provide to expert.

                The answer will be returned as a response, and it will be in the following format:

                [n] "tool_name": {ToolTypeNames.EXPERT_NETWORK_QUERY_CALL},
                    [na.] "tool_response": <sample response>,
                    [ib.] "file_uris": ["...", "..."],
                    [ic.] "image_uris": ["...", "..."]

                *Important Note*
                - If you retrieve the response, stop calling the tool again, and instead provide the response to
                user in natural language, using data you received.

                ---
            """
    return response_prompt
