#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: execute_hadron_prime_node_query_tool_prompt.py
#  Last Modified: 2024-11-13 05:16:15
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-13 05:16:36
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


def build_tool_prompt__execute_hadron_prime_node_query():
    response_prompt = f"""

            ### **TOOL**: Hadron Prime Node Query Execution

            - The Hadron Prime Node Query Execution Tool is a tool you can use to retrieve data about the status fo a
            Hadron Prime Node within the Bimod.io ecosystem. Hadron Prime is a system enabling LLM models to control
            robotics systems and IOT devices and a Hadron Node is an independent unit of processing within Bimod ecosystem.
            Each node at every processing step calculates the inputs, states, measurements, and other parameters to decide
            on an action and share their actions with other nodes using messaging topics. When you are communicating with
            a Hadron node using this tool, the assistant you are communicating with will return data about it's current
            status to you in natural language so you can answer user's questions about robotic systems based on the answer
            of the nodes. You can try to reach any of the specified Hadron Nodes that is defined within your
            "Hadron Prime Node <> Assistant Connections" section.

            - The format for the dictionary you will output to use Hadron Prime Node Query Execution is as follows:

            '''
                {{
                    "tool": "{ToolCallDescriptorNames.EXECUTE_HADRON_PRIME_NODE_QUERY}",
                    "parameters": {{
                        "connection_id": "...",
                        "query": "...",
                        }}
                    }}
            '''

            ---

            #### **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            #### **INSTRUCTIONS:** The "connection_id" will be the ID of Hadron Prime Node <> Assistant Connection object
            you are referring to for executing your query, and "query" will be the query you are investigating in natural
            language for the Hadron Node assistant to answer.

            To use this tool, you need to provide following fields 'VERY CAREFULLY':

            - [1] The "query" field must be the query you are investigating in natural language for the Hadron Node assistant
            to answer. This query will be used to retrieve the information from the Hadron Node you are referring to. For
            example; you can ask "What is the current status of the Hadron Node?" or "What are the recent actions of the
            Hadron Node?".

            #### **NOTE**: The system will provide you the results of search in the next 'assistant' message.
            This message will have the output of the agent you are communicating with in natural language. You are
            expected to take in this response, and use it to provide an answer to the user.

            ---

        """

    return response_prompt
