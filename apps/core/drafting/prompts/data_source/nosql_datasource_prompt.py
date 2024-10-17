#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: nosql_datasource_prompt.py
#  Last Modified: 2024-10-16 01:33:16
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-16 01:35:53
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from apps.assistants.models import Assistant
from apps.datasource_nosql.models import NoSQLDatabaseConnection, CustomNoSQLQuery


def build_drafting_nosql_data_source_prompt(assistant: Assistant):
    nosql_data_sources = NoSQLDatabaseConnection.objects.filter(assistant=assistant)
    response_prompt = """
        ### **NO-SQL DATABASE CONNECTIONS:**

        '''
        """

    for i, nosql_data_source in enumerate(nosql_data_sources):
        nosql_data_source: NoSQLDatabaseConnection
        custom_queries_of_datasource = nosql_data_source.custom_queries.all()
        response_prompt += f"""
        [NoSQL Data Source ID: {nosql_data_source.id}]
            NoSQL DBMS Type: {nosql_data_source.nosql_db_type}
            Bucket Name: {nosql_data_source.bucket_name}
            Description: {nosql_data_source.description}
            Do you have Read Access: YES
            Do you have Write Access: {not nosql_data_source.is_read_only}
            Maximum Records to Retrieve / Query (LIMIT): {nosql_data_source.one_time_retrieval_instance_limit}
            Bucket Schema:
            '''
            {nosql_data_source.schema_data_json}
            '''

            #### **Custom Queries of this Data Source:**
            ---

        """

        for j, custom_query in enumerate(custom_queries_of_datasource):
            custom_query: CustomNoSQLQuery
            response_prompt += f"""
            [Custom NoSQL Query ID: {custom_query.id}]
                NoSQL Query Data Source ID: {custom_query.database_connection.id}
                NoSQL Query Name: {custom_query.name}
                NoSQL Query Description: {custom_query.description}
                NoSQL Query Content:
                '''
                {custom_query.nosql_query}
                '''
            """

    response_prompt += """
        '''

        ---

         #### **NOTE**: These are the NoSQL Database Connections that you have access. Keep these in mind while
        responding to user. Custom queries are also provided for each NoSQL Connection, which you can use to fetch
        data from the respective database or if you have the write permissions, you can use them to write data as well.
        If this part is EMPTY, it means that the user has not provided any NoSQL Database Connections (yet), so
        neglect this part.

        #### **NOTE about Bucket Schema:** The Bucket Schema is provided for your reference to help you understand what
        kind of data types and tables are available in the respective database.

        #### **NOTE ABOUT RETRIEVAL LIMITS**: The user has specified limits for 'read' operations within
        the 'Maximum Records to Retrieve / Query (LIMIT)' field. Please make sure to follow the limits when
        executing the NoSQL queries by always embedding the 'LIMIT' clause in your queries, even if they are
        not present in a custom query. This is very important to ensure that the system does not overload the
        DB with a large number of records.

        ---

        """

    return response_prompt
