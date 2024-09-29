#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: build_sql_query_execution_tool_prompt.py
#  Last Modified: 2024-09-28 00:42:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:12:12
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from apps._services.tools.utils import ToolTypeNames


def build_structured_tool_prompt__sql_query_execution():
    response_prompt = f"""
        **TOOL**: SQL Query Execution

        - The SQL Query Execution Tool is a tool that you can use to execute SQL queries on the SQL Database
        Connections that you have access to. This tool is very useful when you need to fetch data from the
        SQL Database Connections to provide a more accurate response to the user's questions.

        - The standardized format for the dictionary that you will output to use the SQL Query Execution Tool
        is as follows:

        '''
            {{
                "tool": "{ToolTypeNames.SQL_QUERY_EXECUTION}",
                "parameters": {{
                    "database_connection_id": "...",
                    "sql_query": "...",
                    "type": "read" or "write"
                    }}
                }}
        '''

        **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

        **INSTRUCTIONS:** The "database_connection_id" will be the ID of the SQL Database Connection that you
        would like to execute the SQL query on, and the "sql_query" will be the SQL query that you would like to
        execute. The "type" will be either "read" or "write" based on the type of query you would like to execute.

        - For executing the SQL queries, you have 2 choices:

            1. You can choose a query from the custom queries provided for the SQL Database Connection,
            put it in the "sql_query" parameter of the JSON for the system to execute and provide you the
            results in the next 'assistant' message.

            2. If you believe the custom queries are not suitable for the user's request, you can design/write
            your OWN SQL queries to fetch data from the SQL Database Connections. However, be aware of the fact
            that not all database connections have write permissions, so make sure to check the permissions
            before executing those queries.

    """
    return response_prompt
