#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: voidforger_action_history_log_search_prompt.py
#  Last Modified: 2024-11-16 00:53:39
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-16 00:53:47
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


def build_structured_tool_prompt__action_history_log_search_voidforger():
    response_prompt = f"""
        ### **TOOL: Action History Log Search Tool**

        - This tool allows you to retrieve your previous actions through your execution cycles. You can use this
        tool to understand the actions you have previously taken, and then decide on your next actions based on
        understanding these and considering your overall objectives.

        - To use this tool, you must provide a query to search with the action history logs. Your query will be searched
        within the fields of the action logs, which contain:
            i. Action Type: Either a previous output you had in natural language, or a tool call you previously made.
            ii. Action Raw Text: The raw text of the action you took, which can be a tool call or a natural language output.
            iii. Action Timestamp: The timestamp of the action you took.

        -----

        - The format of dict to use for searching the action history logs is as follows:

        '''
            {{
                "tool": "{ToolCallDescriptorNames.EXECUTE_VOIDFORGER_ACTION_HISTORY_LOG_SEARCH_QUERY}",
                "parameters": {{
                    "query": "<your search query here>"
                }}
            }}
        '''

        ---

        #### **INSTRUCTIONS**

        - "query" is the field where you will provide the search query to search within the action history logs.

        The answer will be returned as a response, and it will be in the following format:

        [n] "tool_name": {ToolCallDescriptorNames.EXECUTE_VOIDFORGER_ACTION_HISTORY_LOG_SEARCH_QUERY},
            [na.] "tool_response": <sample response>,
            [ib.] "file_uris": ["...", "..."],
            [ic.] "image_uris": ["...", "..."]

        ---
    """
    return response_prompt
