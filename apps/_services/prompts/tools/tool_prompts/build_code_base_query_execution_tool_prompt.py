#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#

from apps._services.tools.utils import ToolTypeNames


def build_structured_tool_prompt__code_base_query_execution():
    response_prompt = f"""
            **TOOL**: Code Base Search Query Execution

            - The Code Base Query Execution Tool is a tool you can use to search within the connected code base repositories
            of the user to provide a more accurate response to the user's questions. You can try to reach any of the
            specified knowledge bases defined within the "Code Base Storage Connections" section.

            - The standardized format for the dictionary that you will output to use the Code Base Query Execution
            Tool is as follows:

            '''
                {{
                    "tool": "{ToolTypeNames.CODE_BASE_QUERY_EXECUTION}",
                    "parameters": {{
                        "code_base_storage_connection_id": "...",
                        "query": "...",
                        "alpha": 0.0 <= value_of_alpha <= 1.0,
                        }}
                    }}
            '''

            **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            **INSTRUCTIONS:** The "code_base_storage_connection_id" will be the ID of the Code Base Storage Connection that
            you would like to execute your query on, and the "query" will be the string that you would like to search
            within the code base storage repositories. The "alpha" parameter is a float value between 0.0 and 1.0 that
            determines the weight of semantic versus keyword-based search in the search algorithm:

            - An alpha of 1.0 means that the search will be purely vector-based (semantic) search.
            - An alpha of 0.0 means that the search will be purely keyword-based search.
            - Thus, the value of alpha can be adjusted between float values of 0.0 and 1.0 to adjust the balance
            between semantic and keyword-based search, according to the question of the user and your judgment.

            To use this tool, you need to provide the following fields for the system 'VERY CAREFULLY':

            1. The "query" field should be a string that you would like to search within the code base storage repositories.
            This string can be a question or a keyword that you would like to search within the repositories.

            2. The "alpha" field should be a float value between 0.0 and 1.0 that determines the weight of semantic
            versus keyword-based search in the search algorithm.

            **NOTE**: The system will provide you with the results of the search in the next 'assistant' message.
            This message will have a list of repository contents that are most relevant to the query you have provided.
            The fields will include "chunk_repository_file_name", which is the name of the repository content that contains
            the retrieved information; "chunk_number", which is the number of the chunk within the repository (ordered)
            that contains the retrieved information; and "chunk_content", which is the text of the chunk that
            contains the retrieved information (which is the primary field that you will use to search answers
            for the user).

            - You are expected to take in this response, and use it to provide an answer to the user's question.

        """
    return response_prompt
