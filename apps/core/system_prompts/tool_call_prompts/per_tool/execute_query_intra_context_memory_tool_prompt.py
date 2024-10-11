#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: execute_query_intra_context_memory_tool_prompt.py
#  Last Modified: 2024-10-05 02:26:00
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:35
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#


from apps.core.tool_calls.utils import ToolCallDescriptorNames


def build_tool_prompt__intra_context_memory():
    response_prompt = f"""
        ### **TOOL**: Vector Chat History (Long Term Memory) Query Execution

        - The Vector Chat History Query Execution Tool is a tool you can use to search within your chat history
        with user, as this is a vector-based tool, it has almost infinite capacity for you to bypass the limits of
        your 'context window'.

        - The format for dictionary you will output to use Vector Chat History Query Execution Tool is as follows:

        '''
            {{
                "tool": "{ToolCallDescriptorNames.EXECUTE_INTRA_MEMORY_QUERY}",
                "parameters": {{
                    "query": "...",
                    "alpha": 0.0 <= value_of_alpha <= 1.0,
                    }}
                }}
        '''

        ---

        #### **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

        #### **INSTRUCTIONS:** The "query" will be the string you need to search in your chat history with user.
        The "alpha" parameter is a float value between 0.0 and 1.0 determining the weight of semantic versus
        keyword-based search in search algorithm:

            - An alpha of 1.0 means your search will be purely vector-based (semantic) search.
            - An alpha of 0.0 means your search will be purely keyword-based.
            - Thus, the value of alpha can be adjusted between float values of 0.0 and 1.0 to adjust balance
            between semantic and keyword-based search, according to question of user and your judgment.

        To use this, you need to provide following fields 'VERY CAREFULLY':

        - [1] The "query" field must be a string you need to search in the memory documents.
        This string can be a question or a keyword that you would like to search within the memory.

        - [2] The "alpha" field must be a float value between 0.0 and 1.0 determining the weight of semantic
        versus keyword-based search in the search algorithm.

        #### **NOTE**: The system will provide you the results of search in the next 'assistant' message.
        This message will have a list of memories most relevant to the query you provided. The fields will include:
        "chunk_number", which is number of the chunk within the document (ordered) that contains the retrieved
        info; and "chunk_content", which is the text of the chunk that contains the retrieved memory in textual format.

            - You are expected to take in this response, and use it to provide answer to user's question.

            - You MUST use this, if user asks you a question you don't remember the answer to. This probably means
            that your 'context window' has been exceeded, and some of the oldest messages you had was removed from the
            history. Thus, sometimes you must use this tool to search within your long-term memory to provide an
            accurate response to user's questions.

    """
    return response_prompt
