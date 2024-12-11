#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: harmoniq_tools_expert_networks_query_prompt.py
#  Last Modified: 2024-10-05 02:25:59
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:35
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


def build_structured_tool_usage_instructions_prompt_harmoniq():
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
