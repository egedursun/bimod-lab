#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: execute_metakanban_query_tool_prompt.py
#  Last Modified: 2024-11-13 05:16:26
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


def build_tool_prompt__execute_metakanban_query():
    response_prompt = f"""

            ### **TOOL**: MetaKanban Query Execution

            - The MetaKanban Query Execution Tool is a tool you can use to command orders and manage the AI Kanban board
            manager assistant within the Bimod.io ecosystem by providing orders/queries in natural language. MetaKanban is
            an AI-assistant Kanban board that contains tasks, columns, labels that can be managed by an AI assistant that
            takes inputs in natural language and then performs certain actions to update the Kanban board. This AI assistant
            is also be able to record and access latest meeting records and can integrate the meeting records to the Kanban
            board whenever requested. When you are communicating with a MetaKanban assistant using this tool, the manager
            assistant will return responses about it's current status to you in natural language so you can answer
            user's questions about the MetaKanban board as well as understanding the actions taken by that assistant.
            You can try to reach any of the specified MetaKanban board connections that is defined within your
            "MetaKanban <> Assistant Connections" section.

            - The format for the dictionary you will output to use MetaKanban Query Execution Tool is as follows:

            '''
                {{
                    "tool": "{ToolCallDescriptorNames.EXECUTE_METAKANBAN_QUERY}",
                    "parameters": {{
                        "connection_id": "...",
                        "query": "...",
                        }}
                    }}
            '''

            ---

            #### **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            #### **INSTRUCTIONS:** The "connection_id" will be the ID of MetaKanban <> Assistant Connection object
            you are referring to for executing your query, and "query" will be the query you are investigating in natural
            language for the MetaKanban assistant to answer, or the command you are providing to the MetaKanban assistant
            to execute an action on the Kanban board.

            To use this tool, you need to provide following fields 'VERY CAREFULLY':

            - [1] The "query" field must be the query you are investigating in natural language for the MetaKanban assistant
            to answer, or the command you are providing to the MetaKanban assistant to execute an action on the Kanban board.
            This query will be used to retrieve the information from the MetaKanban assistant you are referring to. For
            example; you can ask "What is the current status of the Kanban board?" or "Add a new task to the To Do column
            for fixing the nasty bug project X", or "Integrate the latest meeting to the Kanban board".

            #### **NOTE**: The system will provide you the results of search in the next 'assistant' message.
            This message will have the output of the agent you are communicating with to manipulate MetaKanban boards. You are
            expected to take in this response, and use it to provide an answer to the user.

            ---

        """

    return response_prompt
