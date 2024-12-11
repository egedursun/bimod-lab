#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: build_knowledge_base_query_execution_tool_prompt.py
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

from apps.core.tool_calls.utils import (
    ToolCallDescriptorNames
)


def build_tool_prompt__query_vector_store():
    response_prompt = f"""

            ### **TOOL**: Knowledge Base Document Search Query Execution

            - The Knowledge Base Query Execution Tool is a tool you can use to search within the uploaded documents
            of user to provide more accurate responses to user's questions. You can try to reach any of the
            specified knowledge bases defined within the "Knowledge Base Connections" section.

            - The format for the dictionary you will output to use Knowledge Base Query Execution Tool is as follows:

            '''
                {{
                    "tool": "{ToolCallDescriptorNames.EXECUTE_VECTOR_STORE_QUERY}",
                    "parameters": {{
                        "knowledge_base_connection_id": "...",
                        "query": "...",
                        "alpha": 0.0 <= value_of_alpha <= 1.0,
                        }}
                    }}
            '''

            ---

            #### **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            #### **INSTRUCTIONS:** The "knowledge_base_connection_id" will be the ID of Knowledge Base Connection
            you need to execute your query on, and "query" will be the string you need to search within the knowledge
            base documents. The "alpha" is a float value between 0.0 and 1.0 determining the weight of semantic
            versus keyword-based search in search algorithm:

                - An alpha of 1.0 means the search will be purely vector-based (semantic) search.
                - An alpha of 0.0 means the search will be purely keyword-based.
                - Thus, the value of alpha can be adjusted between float values of 0.0 and 1.0 to adjust balance
                between semantic and keyword-based search, according to question of user and your judgment.

            To use this, you need to provide following fields 'VERY CAREFULLY':

            - [1] The "query" must be a string you need to search within knowledge base documents. This string can be
            a question or a keyword you need to search within documents.

            - [2] The "alpha" must be a float value between 0.0 and 1.0 determining the weight of semantic versus
            keyword-based search in search algorithm.

            ---

            #### **NOTE**: The system will provide you the results of search in next 'assistant' message.
            This message will have a list of documents most relevant to query you provided. The fields will
            include "chunk_document_file_name", which is name of the document containing the retrieved information;
            "chunk_number", which is the no of the chunk within the document (ordered) containing the retrieved
            info; and "chunk_content", which is text of the chunk containing the retrieved info (which is the primary
            field you need to search answers for user). You are expected to take in this response, and use it to
            provide an answer to user's question.

            ---

        """

    return response_prompt
