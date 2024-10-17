#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: build_code_base_query_execution_tool_prompt.py
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
#   For permission inquiries, please contact: admin@Bimod.io.
#


from apps.core.tool_calls.utils import ToolCallDescriptorNames


def build_tool_prompt__execute_codebase_query():
    response_prompt = f"""

            ### **TOOL**: Code Base Search Query Execution

            - The Code Base Query Execution Tool is a tool you can use to search within the connected code base
            repositories of user to provide more accurate responses to their questions. You can try to reach any of the
            specified code bases defined within the "Code Base Storage Connections" section.

            - The format for the dictionary you will output to use Code Base Query Execution Tool is as follows:

            '''
                {{
                    "tool": "{ToolCallDescriptorNames.EXECUTE_CODE_BASE_QUERY}",
                    "parameters": {{
                        "code_base_storage_connection_id": "...",
                        "query": "...",
                        "alpha": 0.0 <= value_of_alpha <= 1.0,
                        }}
                    }}
            '''

            ---

            #### **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            #### **INSTRUCTIONS:** The "code_base_storage_connection_id" will be the ID of Code Base Storage Connection
            you need to execute your query, and "query" will be the string you need to search within the code base
            storage repos. The "alpha" is a float value between 0.0 and 1.0 that determines the weight of semantic
            versus keyword-based search in search algorithm:

                - An alpha of 1.0 means the search will be purely vector-based (semantic) search.
                - An alpha of 0.0 means the search will be purely keyword-based.
                - Thus, value of alpha can be adjusted between float values of 0.0 and 1.0 to adjust the balance
                between semantic and keyword-based search, according to question of user and your judgment.

            To use this, you need to provide following fields 'VERY CAREFULLY':

            - [1] The "query" field should be a string that you would like to search within the code base storage repositories.
            This string can be a question or a keyword that you would like to search within the repositories.

            - [2] The "alpha" field should be a float value between 0.0 and 1.0 that determines the weight of semantic
            versus keyword-based search in the search algorithm.

            #### **NOTE**: The system will provide you the results of search in the next 'assistant' message.
            This message will have a list of repository contents that are most relevant to query you have provided.
            The fields will include "chunk_repository_file_name", which is name of the repository content containing
            retrieved information; "chunk_number", which is the number of the chunk within repository (ordered)
            containing retrieved information; and "chunk_content", which is the text of the chunk containing the
            retrieved information (which is the primary field you will use to search answers for user). You are
            expected to take in this response, and use it to provide an answer.

            ---

        """
    return response_prompt
