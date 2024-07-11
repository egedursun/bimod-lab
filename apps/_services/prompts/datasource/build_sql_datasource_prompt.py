from django.contrib.auth.models import User

from apps.assistants.models import Assistant
from apps.datasource_sql.models import SQLDatabaseConnection


def build_sql_datasource_prompt(assistant: Assistant, user: User):
    response_prompt = ""
    # Gather the SQL datasource connections of the assistant
    sql_datasources = SQLDatabaseConnection.objects.filter(assistant=assistant)
    # Build the prompt
    response_prompt = """
        **SQL DATABASE CONNECTIONS:**

        '''
        """

    for i, sql_datasource in enumerate(sql_datasources):

        custom_queries_of_datasource = sql_datasource.custom_queries.all()

        response_prompt += f"""
        [SQL Datasource ID: {sql_datasource.id}]
            DBMS System Type: {sql_datasource.dbms_type}
            Database Name: {sql_datasource.database_name}
            Database Description: {sql_datasource.description}
            Do you have Read Permissions: YES
            Do you have Write Permissions: {not sql_datasource.is_read_only}
            DBMS Schema for your Reference:
            '''
            {sql_datasource.schema_data_json}
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
        """

    return response_prompt
