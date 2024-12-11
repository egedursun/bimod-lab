#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: voidforger_tools_instructions_prompt.py
#  Last Modified: 2024-11-16 00:52:46
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-16 00:52:47
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

def build_structured_tool_usage_instructions_prompt_voidforger():
    response_prompt = """
        ### **TOOL USAGE**

        - As the VoidForger, you can use tools to search through your knowledge and/or give commands and orders to
        your underlying LeanMod oracles.

        - You have 2 options:

            - [1] You can provide responses directly: Do it only if you have enough data or completed the overall objective
            of your cycle depending on your plan. This kind of response is delivered in natural language.

            - [2] You can output a JSON tool call, which will be used to call the relevant tool.
                - Based on the tool type, system will execute the tool, and provide an output in a new message with role 'assistant'.

        - Format of a tool call:

        '''
        {
            "tool": "name here",
            "parameters": {
                "param1": "value1",
                "param2": "value2",
                ...
        }
        '''

        - "tool" is name of tool you need to use.
        - "parameters" are parameters that tool requires.
        - For each tool, specific explanations are also shared in your prompt.
    """

    return response_prompt
