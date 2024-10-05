#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: build_sql_data_source_prompt.py
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#

from apps.assistants.models import Assistant
from apps.datasource_sql.models import SQLDatabaseConnection


def build_sql_data_source_prompt(assistant: Assistant):
    # Gather the SQL datasource connections of the assistant
    sql_data_sources = SQLDatabaseConnection.objects.filter(assistant=assistant)
    # Build the prompt
    response_prompt = """
        **SQL DATABASE CONNECTIONS:**

        '''
        """

    for i, sql_data_source in enumerate(sql_data_sources):
        custom_queries_of_datasource = sql_data_source.custom_queries.all()
        response_prompt += f"""
        [SQL Data Source ID: {sql_data_source.id}]
            DBMS System Type: {sql_data_source.dbms_type}
            Database Name: {sql_data_source.database_name}
            Database Description: {sql_data_source.description}
            Do you have Read Permissions: YES
            Do you have Write Permissions: {not sql_data_source.is_read_only}
            Maximum Records to Retrieve per Query (LIMIT): {sql_data_source.one_time_sql_retrieval_instance_limit}
            DBMS Schema for your Reference:
            '''
            {sql_data_source.schema_data_json}
            '''

            **Custom Queries of this Datasource:**
            -------

        """

        for j, custom_query in enumerate(custom_queries_of_datasource):
            response_prompt += f"""
            [Custom Query ID: {custom_query.id}]
                Query Data Source ID: {custom_query.database_connection.id}
                Query Name: {custom_query.name}
                Query Description: {custom_query.description}
                SQL Query:
                '''
                {custom_query.sql_query}
                '''
            """

    response_prompt += """
        -------

        '''

        **NOTE**: These are the SQL Database Connections that you have access to. Make sure to keep these in mind
        while responding to the user's messages. Custom queries are also provided for each SQL Database Connection,
        which you can use to fetch data from the respective database or if you have the write permissions, you
        can use them to write data to the respective database. If this part is EMPTY, it means that the user has
        not provided any SQL Database Connections, so neglect this part if that is the case.

        **NOTE about DBMS Schema:** The DBMS Schema is provided for your reference to help you understand what
        kind of data types and tables are available in the respective database.

        **NOTE about RETRIEVAL LIMITS**: The user has specified limits for 'read' operations within
        the 'Maximum Records to Retrieve per Query (LIMIT)' field. Please make sure to follow these limits when
        executing the SQL queries by always embedding the 'LIMIT' clause in your SQL queries, even if they are
        not present in a custom query. This is very important to ensure that the system does not overload the
        database with a large number of records.
        """

    return response_prompt


def build_lean_sql_data_source_prompt():
    # Build the prompt
    response_prompt = """
        **SQL DATABASE CONNECTIONS:**

        '''
        <This data is redacted because you won't need it to serve your instructions.>
        '''

        **NOTE**: These are the SQL Database Connections that you have access to. Make sure to keep these in mind
        while responding to the user's messages. If this part is EMPTY, it means that the user has
        not provided any SQL Database Connections, so neglect this part if that is the case.

        **NOTE about DBMS Schema:** The DBMS Schema is provided for your reference to help you understand what
        kind of data types and tables are available in the respective database.

        **NOTE about RETRIEVAL LIMITS**: The user has specified limits for 'read' operations within
        the 'Maximum Records to Retrieve per Query (LIMIT)' field. Please make sure to follow these limits when
        executing the SQL queries by always embedding the 'LIMIT' clause in your SQL queries, even if they are
        not present in a custom query. This is very important to ensure that the system does not overload the
        database with a large number of records.
        """

    return response_prompt
