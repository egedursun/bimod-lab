#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: execute_instant_connection_prompt.py
#  Last Modified: 2025-01-28 15:29:31
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2025-01-28 15:29:32
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


def build_tool_prompt__execute_instant_connection_query():
    response_prompt = f"""
        ### **TOOL**: Instant Connection Query Execution

        - The Instant Connection Query Execution Tool is a tool you can use to execute SQL, NoSQL queries, or SSH
        server commands for resources you don't have direct access to within your defined set of database connections,
        or file system connections via SSH.

        - The format for dictionary you will output to use Instant Connection Query Execution Tool is as follows:

        '''
            {{
                "tool": "{ToolCallDescriptorNames.EXECUTE_INSTANT_CONNECTION_QUERY}",
                "parameters": {{
                    "connection_string": "...",
                    "query_command": "...",
                    }}
                }}
        '''

        [1] How 'connection_string' must be defined:

        <type>.<subtype>://<username>:<password>@<host>:<port>/<database_name>

        where:
            type: The type of connection. Must be within these options: 'sql', 'nosql', 'server'.
            subtype: The subtype of connection. These can be defined separately for each type.
                - For 'sql' type, subtype can be one of these: 'mysql', 'postgresql', 'mssql', 'oracle', 'mariadb'.
                - For 'nosql' type, subtype can be one of these: 'mongodb', 'couchbase', 'neo4j', 'elasticsearch', 'redis', 'weaviate'.
                - For 'server' type, subtype can be one of these: 'ssh'.
            username: The username for the connection.
            password: The password for the connection.
            host: The host for the connection.
            port: The port for the connection.
            database_name: The database for the connection. For SSH connections, this field must not be defined.

        **Never modify the format of the connection string and make sure to define the connection string correctly.**

        Examples:

        - For SQL connections:
            1. sql.mysql://root:password@100.100.0.0.com:3306/mydatabase
            2. sql.postgresql://postgres:password@localhost:5432/mydatabase
            3. sql.mssql://sa:password@localhost:1433/mydatabase
            4. sql.oracle://system:password@localhost:1521/mydatabase
            5. sql.mariadb://root:password@localhost:3306/mydatabase

        - For NoSQL connections:
            1. nosql.mongodb://admin:password@localhost:27017/mydatabase
            2. nosql.couchbase://admin:password@localhost:8091/mydatabase
            3. nosql.neo4j://neo4j:password@localhost:7687/mydatabase
            4. nosql.elasticsearch://elastic:password@localhost:9200/mydatabase
            5. nosql.redis://redis:password@localhost:6379/mydatabase
            6. nosql.weaviate://admin:password@localhost:8080/mydatabase

        - For SSH connections:
            1. server.ssh://root:password@localhost:22

        *Note:* If a field must not be required for a connection, for example 'port', you can leave a placeholder there
        such as 'xxx' to indicate explicitly that the field is not required.

        Example:

             1. sql.mysql://root:password@localhost:xxx/mydatabase
             2. nosql.mongodb://admin:password@localhost:xxx/mydatabase
            3. server.ssh://root:password@localhost:xxx

        [2] How 'query_command' must be defined:

        - For SQL and NoSQL connections, the query command must be the SQL or NoSQL query you want to execute
        on the connection. You already have explanations regarding how to utilize queries for different database
        connections in your prompt.

        - For SSH connections, the query command must be the command you want to execute on the SSH server. If you need
        multiple commands to execute, you can connect them using pipes or semicolons, but your command must be a single
        string and must not contain any line breaks. Otherwise the system will not be able to execute the command.

        ---

        #### **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

        #### **INSTRUCTIONS:** The "connection_string" will be the connection string of the resource you want to execute
        the query on, and "query_command" will be the query you want to execute. Make sure to define the connection
        string and query command correctly to get the desired results.

        - For executing the queries / commands, you have 2 choices:

            - [1] You can choose a query from custom queries provided for SQL, NoSQL, or File System connections, put it in
             "sql_query" parameter of JSON for the system to execute and provide you results in the next
             'assistant' message.

            - [2] If you believe custom queries are not suitable for user's request, you can design/write
            your OWN queries or commands to fetch data from the custom instant Connections. Yet, be aware of the fact that not
            all connections have write permissions, so make sure to check permissions before executing the
            queries.

        ---

    """

    return response_prompt

