#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: build_vectorized_context_history_query_execution_tool_prompt.py
#  Last Modified: 2024-09-28 22:17:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:34
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: build_vectorized_context_history_query_execution_tool_prompt.py
#  Last Modified: 2024-09-28 00:42:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:12:21
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from apps._services.tools.utils import ToolTypeNames


def build_structured_tool_prompt__vectorized_context_history__query_execution_tool_prompt():
    response_prompt = f"""
        **TOOL**: Vector Chat History (Long Term Memory) Query Execution

        - The Vector Chat History Query Execution Tool is a tool you can use to search within your chat history
        with the user, as this is a vector-based tool, it has almost infinite capabilities for you to bypass the
        limits of your 'context window'.

        - The standardized format for the dictionary that you will output to use the Vector Chat History Query Execution
        Tool is as follows:

        '''
            {{
                "tool": "{ToolTypeNames.VECTOR_CHAT_HISTORY_QUERY_EXECUTION}",
                "parameters": {{
                    "query": "...",
                    "alpha": 0.0 <= value_of_alpha <= 1.0,
                    }}
                }}
        '''

        **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

        **INSTRUCTIONS:** The "query" field will be the string that you would like to search within your chat history
        with the user. The "alpha" parameter is a float value between 0.0 and 1.0 that determines the weight of
        semantic versus keyword-based search in the search algorithm:

        - An alpha of 1.0 means that your search will be purely vector-based (semantic) search.
        - An alpha of 0.0 means that your search will be purely keyword-based search.
        - Thus, the value of alpha can be adjusted between float values of 0.0 and 1.0 to adjust the balance
        between semantic and keyword-based search, according to the question of the user and your judgment.

        To use this tool, you need to provide the following fields for the system 'VERY CAREFULLY':

        1. The "query" field should be a string that you would like to search within the knowledge base documents.
        This string can be a question or a keyword that you would like to search within the documents.

        2. The "alpha" field should be a float value between 0.0 and 1.0 that determines the weight of semantic
        versus keyword-based search in the search algorithm.

        **NOTE**: The system will provide you with the results of the search in the next 'assistant' message.
        This message will have a list of memories that are most relevant to the query you have provided. The
        fields will include: "chunk_number", which is the number of the chunk within the document (ordered)
        that contains the retrieved information; and "chunk_content", which is the text of the chunk that
        contains the retrieved memory in textual format.

        - You are expected to take in this response, and use it to provide an answer to the user's question.

        - You MUST use this tool, if the user asks you a question that you don't remember the answer to. This probably
        means that your 'context window' has been exceeded, and some of the messages you had was removed from the
        context history. Therefore, you must use this tool to search within your long-term memory to provide an
        accurate response to the user's question.

    """
    return response_prompt
