#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: build_sql_query_execution_tool_prompt.py
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


def build_tool_prompt__execute_sql_query():
    response_prompt = f"""
        ### **TOOL**: SQL Query Execution

        - The SQL Query Execution Tool is a tool you can use to execute SQL queries on SQL Database Connections you
        have access to. This tool is useful when you need to fetch data from SQL Database Connections to provide
        more accurate responses to user's questions.

        - The format for dictionary you will output to use SQL Query Execution Tool is as follows:

        '''
            {{
                "tool": "{ToolCallDescriptorNames.EXECUTE_SQL_QUERY}",
                "parameters": {{
                    "database_connection_id": "...",
                    "sql_query": "...",
                    "type": "read" or "write"
                    }}
                }}
        '''

        ---

        #### **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

        #### **INSTRUCTIONS:** The "database_connection_id" will be the ID of SQL Database Connection you
        need to execute the SQL query on, and "sql_query" will be SQL query you need to execute. The "type" will
        be either "read" or "write" based on type of query you want to execute.

        - For executing the SQL queries, you have 2 choices:

            - [1] You can choose a query from custom queries provided for SQL Database Connection, put it in
             "sql_query" parameter of JSON for the system to execute and provide you results in the next
             'assistant' message.

            - [2] If you believe custom queries are not suitable for user's request, you can design/write
            your OWN SQL queries to fetch data from SQL Database Connections. Yet, be aware of the fact that not
            all database connections have write permissions, so make sure to check permissions before executing the
            queries.

        ---

    """
    return response_prompt
