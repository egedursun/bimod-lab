#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: execute_nosql_query_tool_prompt.py
#  Last Modified: 2024-10-12 17:41:04
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-12 17:41:05
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


def build_tool_prompt__execute_nosql_query():
    response_prompt = f"""
        ### **TOOL**: NO-SQL Query Execution

        - The NO-SQL Query Execution Tool is a tool you can use to execute NoSQL queries on NoSQL Database Connections
        you have access to. This tool is useful when you need to fetch data from NoSQL Database Connections to provide
        more accurate responses to user's questions.

        - **THE FORMAT / LANGUAGE OF YOUR QUERIES:**

            - [1] The NOSQL queries you are going to be running MUST depend in the database type you are interacting with:
                For example:
                1. For Couchbase: You must use "N1QL" format.
                2. For MongoDB: You must use "JSON" format.
                3. For Redis: You must use "Redis Command Sets" format.
                4. For ElasticSearch: You must use "ElasticSearch Query" format (JSON if needed and/or adequate).
                5. For Neo4J: You must use "Cypher Query Language" format.
                6. For Weaviate: You must use "GraphQL" format (JSON if needed and/or adequate).

            - [2] DO NOT use incompatible query languages for the database you are interacting with. If you are not sure
                about the query language you need to use, please check the database connection object shared with you in
                your prompt.

            - [3] While running queries, you need to make sure you provide the following correctly:
                    - Schema
                    - Scope
                    - Collection Name
                'depending on the NoSQL database you are interacting with' correctly. If you are not sure about the
                schema, scope, and collection name, please check the schema of the database by using the Data Source
                NoSQL definitions in your prompt.

                Sample Correct Usage (for CouchBase Database type):

                '''
                SELECT * FROM `bucket_name`.`scope_name`.`collection_name` WHERE condition
                '''

                Sample Incorrect Usage:

                '''
                SELECT * FROM `collection_name` WHERE condition
                '''

            - [4] REMEMBER, CouchBase does not use SQL, it uses 'N1QL'. So, make sure you are using the correct syntax
            when interacting with the CouchBase databases.

            - [5] Similarly, MongoDB uses 'MongoDB Query Language (MQL)', Redis uses 'Redis Command Sets', ElasticSearch
            uses 'ElasticSearch Query DSL', Neo4J uses 'Cypher Query Language', and Weaviate uses
            'GraphQL'. Make sure you are using the correct syntax for the database you are interacting with.

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
