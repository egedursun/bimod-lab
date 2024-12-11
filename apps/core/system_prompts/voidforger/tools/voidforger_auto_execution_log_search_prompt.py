#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: voidforger_auto_execution_log_search_prompt.py
#  Last Modified: 2024-11-16 00:54:18
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-16 00:54:19
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


def build_structured_tool_prompt__auto_execution_log_search_voidforger():
    response_prompt = f"""
        ### **TOOL: Auto-Execution Log Search Tool**

        - This tool allows you to retrieve your activation and deactivation states that are triggered by users. You can
        use this tool to understand when you were active, when you were doing a certain task, or when you were in a
        deactivated state.

        - To use this tool, you must provide a query to search with the auto-execution logs. Your query will be searched
        within the fields of the auto-execution logs, which contain:
            i. Action Type: Can be one of the following:
                - activated: Which means you were activated at the specified timestamp by the user.
                - paused: Which means you were paused at teh specified timestamp by the user.
                - end_of_life: Which means you have exhausted the total run cycles you have for an automated execution
                process, so you stopped automatically at the specified timestamp.
            ii. Metadata: Additional information depending on the action type being performed.

        -----

        - The format of dict to use for searching the auto-execution logs is as follows:

        '''
            {{
                "tool": "{ToolCallDescriptorNames.EXECUTE_VOIDFORGER_AUTO_EXECUTION_LOG_SEARCH_QUERY}",
                "parameters": {{
                    "query": "<your search query here>"
                }}
            }}
        '''

        ---

        #### **INSTRUCTIONS**

        - "query" is the field where you will provide the search query to search within the auto-execution logs.

        The answer will be returned as a response, and it will be in the following format:

        [n] "tool_name": {ToolCallDescriptorNames.EXECUTE_VOIDFORGER_AUTO_EXECUTION_LOG_SEARCH_QUERY},
            [na.] "tool_response": <sample response>,
            [ib.] "file_uris": ["...", "..."],
            [ic.] "image_uris": ["...", "..."]

        ---
    """

    return response_prompt
