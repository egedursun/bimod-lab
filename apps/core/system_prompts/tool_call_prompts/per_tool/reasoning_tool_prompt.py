#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: build_reasoning_tool_prompt.py
#  Last Modified: 2024-10-06 20:41:38
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-06 20:41:42
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

from config.settings import MEDIA_URL


def build_tool_prompt__reasoning():
    response_prompt = f"""

            ### **TOOL**: Reasoning Tool

            - The Reasoning Tool is a tool containing a special assistant trained with reinforcement learning to
            perform complex reasoning. These models specialize in thinking before they answer, and can produce a
            long internal chain of thought before responding. This assistant use internal thinking, breaking down
            their understanding of given prompt and considering multiple approaches to generating a response.
            After generating results, model produces an answer as visible completions, and discards internal reasoning
            tokens from its context.

                - [i] You must ONLY use this when you have a complex reasoning task you would like to perform since
                this tool is expensive and MUST NOT be used for handling simple tasks that DON'T require a multi-step
                logical approach to solve the problem.

                - [ii] The best way to approach this is; to ask user whenever you are NOT sure if it's a good
                idea to use the tool given a problem that you have hard time to classify in complexity. In that cases,
                you can let user know about whether or not he/she wants you to delve deeper into the topic and
                perform a deep thought to provide a better answer or not.

                - [iii] Then, act upon user's requests to use this tool, or not.

            ---

            - As this tool includes an LLM agent that works separately, while calling this tool, you will essentially
            give instructions to that agent to provide a solution to user's problem. Yet, please note that this agent
            is NOT capable of interpreting images or files, so for those operations you must reference the other tools
            you have. This assistant is able to purely understand textual inputs.

            - The assistant will give you response in natural language after it completes it's operation, and you
            can use this output to provide a final answer to user's question(s).

            - The format for dictionary you will output to use Reasoning Tool is as follows:

            '''
                {{
                    "tool": "{ToolCallDescriptorNames.EXECUTE_REASONING_PROCESS}",
                    "parameters": {{
                        "query": "..."
                    }}
                }}
            '''

            ---

            #### **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            #### **INSTRUCTIONS:** The "query" must be the operation that you want the reasoning assistant
            to execute. In this field, you need to describe the complex logical/thought-requiring operation you
            would like to perform in natural language. The agent will understand the query you provided and
            execute the reasoning operation based on that.

            To use this, you need to provide the following fields 'VERY CAREFULLY':

            - [1] For "query", provide query you would like the reasoning assistant to perform, in NATURAL LANGUAGE.
                - *Example Queries:*
                    - "Please explain what is the best way to solve an organizational conflict by analyzing the pros
                    and cons of each strategy."
                    - "Please provide a detailed explanation of the best way to optimize the performance of a system
                    by considering the trade-offs between different strategies."
                    - "Please provide a detailed explanation of the best way to reduce the costs of a system by
                    considering the trade-offs between different strategies."

                - You ALWAYS need to provide the queries in the "query" field, and in NATURAL LANGUAGE.

            ---

            **IMPORTANT NOTES:**

            #### **NOTE**: The system will provide you the results in next 'assistant' message. This message will
            have the output of the reasoning execution, and you will be expected to take this and provide an answer to
            user's question based on the response you received, in your own words. Think of this as an employee you are
            instructing to execute a query, and you are expected to take the response of this employee and provide an
            answer to the user's question.

            #### **ABOUT PROVIDING URLS & LINKS:**
            - If you need to provide a direct link to user for reaching files, here is the base
                URL you need to 'DIRECTLY' append the file path to provide an absolute HTTP URL to file:
                - {MEDIA_URL}
            - **NEVER, EVER:** provide a 'relative' path to files. Always provide 'ABSOLUTE' path by
            appending the file path to the base URL.

            ---

        """

    return response_prompt
