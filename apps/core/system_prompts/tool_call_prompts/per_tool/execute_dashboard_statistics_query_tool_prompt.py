#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: execute_dashboard_statistics_query_tool_prompt.py
#  Last Modified: 2024-11-13 05:17:32
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-13 05:17:32
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


def build_tool_prompt__execute_dashboard_statistics_query():
    response_prompt = f"""

            ### **TOOL**: Dashboard Statistics Query Execution

            - The Dashboard Statistics Query Execution Tool is a tool you can use to retrieve the statistics for the user
            and user's organizations, his/her usage patterns within the Bimod platform, and insights and recommendations
            regarding these usage patterns.

            - The format for the dictionary you will output to use Dashboard Statistics Query Execution Tool is as follows:

            '''
                {{
                    "tool": "{ToolCallDescriptorNames.EXECUTE_DASHBOARD_STATISTICS_QUERY}",
                    "parameters": {{ }}
                }}
            '''

            ---

            #### **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            #### **INSTRUCTIONS:** There is no additional parameters required for this tool. You can simply leave the
            parameters field empty and execute the tool to retrieve the statistics for the user and user's organizations,
            his/her usage patterns within the Bimod platform, and insights and recommendations regarding these usage patterns.

            #### **NOTE**: The system will provide you the results of search in the next 'assistant' message.
            This message will have the interpretation of another assistant regarding the statistics and insights
            retrieved from the user's usage patterns within the Bimod platform, and will be delivered in natural
            language. You are expected to take in this response, and use it to provide an answer to the user.

            ---

        """

    return response_prompt
