#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: expert_network_consultancy_tool_prompt.py
#  Last Modified: 2024-10-17 22:43:42
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 22:43:43
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


def build_hadron_prime_structured_tool_prompt__expert_network_query_execution():
    response_prompt = f"""
        ### **TOOL: Expert Network Query Call**

        - This allows consulting to expert networks. If data is not enough to respond, you can check network
        descriptions + instructions of assistants to see if they can answer.

        - The format of dict to use:

        '''
            {{
                "tool": "{ToolCallDescriptorNames.EXECUTE_EXPERT_NETWORK_QUERY}",
                "parameters": {{
                    "assistant_id": "...",
                    "query": "...",
                    "image_urls": ["..."],
                    "file_urls": ["..."]
                }}
            }}
        '''

        ---

        #### **INSTRUCTIONS**

        - "assistant_id" is ID of assistant you want to consult. Find ID of assistant by checking networks /
        assistants you have access.
        - "query" is question/request you want to ask.
        - "image_urls" is list of URLs of images to provide to expert.
        - "file_urls" is list of URLs of files to provide to expert.

        The answer will be returned as a response, and it will be in the following format:

        [n] "tool_name": {ToolCallDescriptorNames.EXECUTE_EXPERT_NETWORK_QUERY},
            [na.] "tool_response": <sample response>,
            [ib.] "file_uris": ["...", "..."],
            [ic.] "image_uris": ["...", "..."]

        #### **Important Note**
            - If you retrieve the response, stop calling the tool again, and instead provide the response to
                user in natural language, using data you received.

        ---
    """
    return response_prompt


def build_hadron_prime_structured_tool_usage_instructions_prompt():
    response_prompt = """
        ### **TOOL USAGE**

        - As assistant, you can use tools to provide accurate responses.

        - You have 2 option:

            - [1] You can provide response to question: Do it if having enough data. Response is delivered in
            natural language.

            - [2] You can output JSON, to request using a 'TOOL'.
                - Based on tool, system executes, and provides output in new message with role 'assistant'.
                - It is yours to decide if response is enough, or if need to use tools again.

        - Format of tool call:

        '''
        {
            "tool": "name here",
            "parameters": {
                "param1": "value1",
                "param2": "value2",
                ...
        }
        '''

        - DO NOT WRITE 'json' in the dict or next ''' elements.
        - "tool" is name of tool you need to use.
        - "parameters" are parameters tool requires.
        - For each tool, sample is provided showing how its called.
    """
    return response_prompt


def verify_hadron_prime_expert_network_query_content(content):
    if "parameters" not in content:
        return """
            The 'parameters' is missing from tool_usage_json. This field is mandatory to use Expert Network Query
            Execution tool.
        """
    ps = content.get("parameters")
    if "assistant_id" not in ps:
        return """
            The 'alpha' field is missing from 'parameters' field in tool_usage_json. This field is mandatory for
            using Expert Network Query Execution tool.
        """
    if "query" not in ps:
        return """
            The 'query' field is missing from 'parameters' field in tool_usage_json. This field is mandatory for
            using Expert Network Query Execution tool.
        """
    if not isinstance(ps.get("image_urls"), list) and ps.get("image_urls") is not None:
        return """
            The 'image_urls' field must be a list of URLs of images.
        """
    if not isinstance(ps.get("file_urls"), list) and ps.get("file_urls") is not None:
        return """
            The 'file_urls' field must be a list of URLs of files.
        """
    return None
