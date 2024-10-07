#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#
from apps._services.tools.utils import ToolTypeNames
from config.settings import MEDIA_URL


def build_structured_tool_prompt__reasoning_process():
    response_prompt = f"""
            **TOOL**: Reasoning Tool

            - The Reasoning Tool is a tool containing a special assistant trained with reinforcement learning to
            perform complex reasoning. These models specialize in thinking before they answer, and can produce a
            long internal chain of thought before responding. This assistant use internal thinking, breaking down
            their understanding of the given prompt and considering multiple approaches to generating a response.
            After generating results, the model produces an answer as visible completions, and discards the
            internal reasoning tokens from its context.

                i. You must ONLY use this tool when you have a complex reasoning task that you would like to
                perform since this tool is expensive and MUST NOT be used for handling tasks that DON'T require
                a multi-step logical approach to solve the problem.

                ii. The best way to approach this situation is to ask the user whenever you are NOT sure if it's a good
                idea to use this tool given a problem that you have hard time to classify in complexity. In that cases,
                you can let the user know about whether or not he/she wants you to delve deeper into this topic and
                perform a deep thought to provide a better answer or not.

                iii. Then, act upon user's requests to use this tool or not.

            - As this tool includes an assistant that works separately, while calling this tool, you will essentially
            give instructions to that assistant to provide a solution to user's problem. However, please note that
            this assistant is NOT capable of interpreting images or files, so for those operations you must reference
            the other tools you have. This assistant is able to purely understand textual inputs.
            - The assistant will give you the response in natural language after it completes it's operation, and you
            can use this output to provide a final answer to user's question(s).

            - The standardized format for the dictionary that you will output to use the Reasoning Tool is as follows:

            '''
                {{
                    "tool": "{ToolTypeNames.REASONING}",
                    "parameters": {{
                        "query": "..."
                    }}
                }}
            '''

            **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            **INSTRUCTIONS:** The "query" field should be the operation that you would like the reasoning assistant
            to execute. In this field, you need to describe the complex logical/thought-requiring operation that you
            would like to perform in natural language. The assistant will understand the query that you provide and
            execute the reasoning operation based on the query that you provide.

            To use this tool, you need to provide the following field 'VERY CAREFULLY':

            1. For "query", provide the query that you would like the reasoning assistant to perform, in NATURAL
            LANGUAGE, ALWAYS.
                - *Example Queries:*
                    - "Please explain what is the best way to solve an organizational conflict by analyzing the pros
                    and cons of each strategy."
                    - "Please provide a detailed explanation of the best way to optimize the performance of a system
                    by considering the trade-offs between different strategies."
                    - "Please provide a detailed explanation of the best way to reduce the costs of a system by
                    considering the trade-offs between different strategies."

                - You always need to provide the queries in the "query" field, and in NATURAL LANGUAGE.

            ---

            **IMPORTANT NOTES:**

            **NOTE**: The system will provide you with the results in the next 'assistant' message. This message will
            have the output of the reasoning execution, and you will be expected to take this response and provide an
            answer to the user's question based on the response that you receive, in your own words. Think of this tool
            as an employee of yours that you are instructing to execute a query on a media item, and you are expected
            to take the response of this employee and provide an answer to the user's question based on the response
            that you receive from this employee.

            **ABOUT YOU PROVIDING LINKS:**
            - If you need to provide a direct link to the user for reaching the files, here is the base
                URL you need to 'DIRECTLY' append the file path to provide an absolute HTTP reference to the file:
                - {MEDIA_URL}
            - **NEVER, EVER:** provide a 'relative' path to the files. Always provide the 'ABSOLUTE' path by
            appending the file path to the base URL.

        """
    return response_prompt
