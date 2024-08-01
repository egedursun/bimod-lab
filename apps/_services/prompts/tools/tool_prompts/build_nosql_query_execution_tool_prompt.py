from apps._services.tools.const import ToolTypeNames


INTRINSIC_ONE_TIME_NOSQL_RETRIEVAL_LIMIT = 100


def build_structured_tool_prompt__nosql_query_execution():
    response_prompt = f"""
        **TOOL**: NO-SQL Query Execution

        - The NO-SQL Query Execution Tool is a tool that you can use to execute NO-SQL queries on the document-based
        Database Connections that you have access to. This tool is very useful when you need to fetch data from the
        SQL Database Connections to provide a more accurate response to the user's questions.

        - The standardized format for the dictionary that you will output to use the No-SQL Query Execution Tool
        is as follows:

        '''
            {{
                "tool": "{ToolTypeNames.NOSQL_QUERY_EXECUTION}",
                "parameters": {{
                    "database_connection_id": "...",
                    "query": "...",
                    "type": "read" or "write"
                    }}
                }}
        '''

        **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

        **INSTRUCTIONS:** The "database_connection_id" will be the ID of the NoSQL Database Connection that you
        would like to execute the query on, and the "query" will be the SQL query that you would like to
        execute. The "type" will be either "read" or "write" based on the type of query you would like to execute.

        - For executing the NoSQL queries, you have 2 choices:

            1. You can choose a query from the custom queries provided for the NoSQL Database Connection,
            put it in the "query" parameter of the JSON for the system to execute and provide you the
            results in the next 'assistant' message.

            2. If you believe the custom queries are not suitable for the user's request, you can design/write
            your OWN queries to fetch data from the NoSQL Database Connections. However, be aware of the fact
            that not all database connections have write permissions, so make sure to check the permissions
            before executing those queries.

        This is how your query is executed in the background, observe it carefully and provide your queries accordingly:

        ```python
        collection = self.db.get_collection(collection_name)
            query_json = query.get('query', {{}})
            cursor = collection.find(query_json)
        ```
                - where 'query' is the JSON query you provide in the 'parameters' field of the JSON file.
                - 'collection_name' is the name of the collection you are querying.
                - 'cursor' is the result of the query execution.

        **IMPORTANT NOTE ABOUT THE RETRIEVAL 'LIMIT'**: The system has an intrinsic limit of
        {INTRINSIC_ONE_TIME_NOSQL_RETRIEVAL_LIMIT}. ALWAYS put a limit on the number of documents you are
        fetching from the NoSQL Database Connections based on this limit. This is to ensure that the system
        does not get overloaded with the data and can provide a quick response to the user. If you don't have enough
        information from the first retrieval, you can always fetch more data in the next assistant messages instead,
        or by using a more use-case specific query.

        !!!
        **VERY IMPORTANT NOTE ABOUT SEARCH DEPTH**:
        - ALWAYS put a 'depth limit' on the NoSQL retrieval queries you are executing.
        - Never retrieve nested information, if you dont get enough information from the 1-st level of structured
        JSON, you can run a separate query for "that specific" item, and retrieve the 2-nd level of structured
        JSON for that item only, and so on.

        In other words:
        1. Start with the 1-st level of structured JSON.
        2. If you dont get enough information from the 1-st level, run a separate query for a specific item that
        you need more information about; and retrieve only the 2-nd level of structured JSON for that item.
        3. Repeat the process until you get enough information, but always narrow down the breadth of the search
        as you go deeper.
        !!!

        ----
    """
    return response_prompt
