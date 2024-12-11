#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: execute_orchestration_trigger_tool_prompt.py
#  Last Modified: 2024-11-13 05:17:15
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-13 05:17:15
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


def build_tool_prompt__execute_orchestration_trigger():
    response_prompt = f"""

            ### **TOOL**: Orchestration Triggering Tool

            - The Orchestration Triggering Tool is a tool you can use to trigger the Orchestration Managers/Maestros
            to let them work on a complex topic. Orchestration is a technique within Bimod.io platform allowing Manager
            AI assistants to organize multiple different assistants specializing in different topics and have different
            multi-modal tools and data sources in their availability to perform a complex task. Orchestration managers
            are responsible for organizing these processes by splitting complex tasks into multiple pieces and then
            assigning these pieces to the relevant assistants in the correct order, then delivering the final results
            to the user. When you are Triggering an orchestrator using this tool, the tool will call the relevant orchestrator
            in the background and the Maestro/Manager for the orchestration will start processing based on your query
            right away. Once the processing is done, you will be able to retrieve the output of these processing, and
            you can answer user's questions about the Orchestrations based on these responses. You can try to trigger any
            of the specified Orchestration Manager/Maestro that is defined within your "Orchestration Manager/Maestro <> Assistant Connections"
            section.

            - The format for the dictionary you will output to use Orchestration Triggering Tool is as follows:

            '''
                {{
                    "tool": "{ToolCallDescriptorNames.EXECUTE_ORCHESTRATION_TRIGGER}",
                    "parameters": {{
                        "connection_id": "...",
                        "query": "..."
                        }}
                    }}
            '''

            ---

            #### **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            #### **INSTRUCTIONS:** The "connection_id" will be the ID of Orchestration Manager/Maestro <> Assistant Connection
            object you are referring to for being triggered for your query, and "query" will be the query you are providing
            for the orchestrator, in other words the complex task you want the orchestrator to work on.

            To use this tool, you need to provide following fields 'VERY CAREFULLY':

            - [1] The "query" field must be the query you are providing for the orchestrator, in other words the complex task
            you want the orchestrator to work on. This query will be used to trigger the orchestrator you are referring to. For
            example; you can ask "Can you please find a blog about the recent trends in AI, prepare a slideshow about 3 most
            important trends, and then summarize the blog in a 500 words article, and finally share the article with my email
            address?" or "Can you please find the recent news about the company X, prepare a report about the news, and then
            share the report with the team members?".

            #### **NOTE**: The system will provide you the results of search in the next 'assistant' message.
            This message will have the output of the orchestration manager you are communicating with and it will inform
            you about the overall output of the orchestration process. You are expected to take in this response, and
            use it to provide a final answer to the user.

            ---

        """

    return response_prompt
