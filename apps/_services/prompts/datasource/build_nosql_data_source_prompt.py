
from apps.assistants.models import Assistant
from apps.datasource_nosql.models import NoSQLDatabaseConnection


def build_nosql_datasource_prompt(assistant: Assistant):
    response_prompt = ""
    # Gather the NoSQL datasource connections of the assistant
    nosql_datasources = NoSQLDatabaseConnection.objects.filter(assistant=assistant)
    # Build the prompt
    response_prompt = """
        **NO-SQL DATABASE CONNECTIONS:**

        '''
        """

    for i, nosql_datasource in enumerate(nosql_datasources):

        custom_queries_of_datasource = nosql_datasource.custom_queries.all()

        response_prompt += f"""
        [NO-SQL Datasource ID: {nosql_datasource.id}]
            System Type: {nosql_datasource.dbms_type}
            NoSQL Database Name: {nosql_datasource.db_name}
            NoSQL Database Description: {nosql_datasource.description}
            Do you have Read Permissions: YES
            Do you have Write Permissions: {not nosql_datasource.is_read_only}
            NoSQL Database Schema for your Reference:
            '''
            {nosql_datasource.schema_data_json}
            '''

            **Custom NoSQL Queries of this Datasource:**
            -------

        """

        for j, custom_query in enumerate(custom_queries_of_datasource):
            response_prompt += f"""
            [Custom NoSQL Query ID: {custom_query.id}]
                NoSQL Query Data Source ID: {custom_query.database_connection.id}
                NoSQL Query Name: {custom_query.name}
                NoSQL Query Description: {custom_query.description}
                NoSQL Query String/JSON:
                '''
                {custom_query.sql_query}
                '''
            """

    response_prompt += """
        -------

        '''

        **NOTE**: These are the NO-SQL Database Connections that you have access to. Make sure to keep these in mind
        while responding to the user's messages. Custom NoSQL queries are also provided for each NoSQL Database
        Connection, which you can use to fetch data from the respective document-based database or if you have the
        write permissions, you can use them to write data to the respective database. If this part is EMPTY,
        it means that the user has not provided any NoSQL/document-based Database Connections, so neglect this part
        if that is the case.

        **NOTE about NoSQL Schema:** The NoSQL DBMS Schema is provided for your reference to help you understand what
        kind of data types and tables are available in the respective database.
        """

    return response_prompt
