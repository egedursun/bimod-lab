#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: nosql_tool_prompts.py
#  Last Modified: 2024-10-16 01:37:01
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-16 01:37:01
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


def build_drafting_tool_prompt__execute_nosql_query():
    response_prompt = f"""
        ### **TOOL**: NO-SQL Query Execution

        - The NO-SQL Query Execution Tool is a tool you can use to execute NoSQL queries on NoSQL Database Connections
        you have access to. This tool is useful when you need to fetch data from NoSQL Database Connections to provide
        more accurate responses to user's questions.

        - **THE FORMAT / LANGUAGE OF YOUR QUERIES:**

            - [1] All NOSQL queries you are going to be running MUST be in "N1QL" format.

            - [2] DO NOT use any other query language than "N1QL" for NoSQL queries.

            - [3] While running queries, you need to make sure you provide the following correctly:
                    - Schema
                    - Scope
                    - Collection name
                correctly. If you are not sure about the schema, scope, and collection name, please check the
                schema of the database by using the Data Source NoSQL definitions in your prompt.

                Sample Correct Usage:

                '''
                SELECT * FROM `bucket_name`.`scope_name`.`collection_name` WHERE condition
                '''

                Sample Incorrect Usage:

                '''
                SELECT * FROM `collection_name` WHERE condition
                '''

            - [4] REMEMBER, this is not SQL, this is 'N1QL'. So, make sure you are using the correct syntax.

        ---

        - The format for dictionary you will output to use NO-SQL Query Execution Tool is as follows:

        '''
            {{
                "tool": "{ToolCallDescriptorNames.EXECUTE_NOSQL_QUERY}",
                "parameters": {{
                    "database_connection_id": "...",
                    "nosql_query": "...",
                    "type": "read" or "write"
                    }}
                }}
        '''

        ---

        #### **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

        #### **INSTRUCTIONS:** The "database_connection_id" will be the ID of NoSQL Database Connection you
        need to execute the NoSQL query on, and "nosql_query" will be NoSQL query you need to execute. The "type" will
        be either "read" or "write" based on type of query you want to execute.

        - For executing the NoSQL queries, you have 2 choices:

            - [1] You can choose a query from custom queries provided for NoSQL Database Connection, put it in
             "nosql_query" parameter of JSON for the system to execute and provide you results in the next
             'assistant' message.

            - [2] If you believe custom queries are not suitable for user's request, you can design/write
            your OWN NoSQL queries to fetch data from NoSQL Database Connections. Yet, be aware of the fact that not
            all database connections have write permissions, so make sure to check permissions before executing the
            queries.

        ---

    """
    return response_prompt
