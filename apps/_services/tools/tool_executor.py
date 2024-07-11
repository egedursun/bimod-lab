import json
import pprint

from apps._services.sql.sql_decoder import InternalSQLClient
from apps._services.tools.const import ToolTypeNames
from apps.assistants.models import Assistant
from apps.datasource_sql.models import SQLDatabaseConnection


def validate_main_tool_json(tool_usage_json: dict):
    ##################################################
    # Check if the JSON is empty
    if not tool_usage_json:
        return """
                    The JSON is empty. Please make sure you are passing the correct JSON object to the
                    ToolDecoder class.
                """
    ##################################################

    ##################################################
    # Check if the tool field is missing
    if not tool_usage_json.get("tool"):
        return """
                    The 'tool' field is missing from the tool_usage_json. Please make sure you are defining the tool
                    name in the tool_usage_json.
                """
    ##################################################

    return None


def validate_sql_query_execution_tool_json(tool_usage_json: dict):
    if "parameters" not in tool_usage_json:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the SQL Query
            Execution tool. Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """
    parameters = tool_usage_json.get("parameters")

    if "sql_query" not in parameters:
        return """
            The 'sql_query' field is missing from the 'parameters' field in the tool_usage_json. This field is
            mandatory for using the SQL Query Execution tool. Please make sure you are defining the 'sql_query' field
            in the parameters field of the tool_usage_json.
        """
    if "database_connection_id" not in parameters:
        return """
            The 'database_connection_id' field is missing from the 'parameters' field in the tool_usage_json. This
            field is mandatory for using the SQL Query Execution tool. Please make sure you are defining the
            'database_connection_id' field in the parameters field of the tool_usage_json.
        """
    if "type" not in parameters:
        return """
            The 'type' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the SQL Query Execution tool. This must either be 'read' or 'write' based on the type of query you
            are executing. Please make sure you are defining the 'type' field in the parameters field of the
            tool_usage_json.
        """
    query_type = parameters.get("type")
    if query_type not in ["read", "write"]:
        return """
            The 'type' field in the 'parameters' field of the tool_usage_json must either be 'read' or 'write'. This
            field is mandatory for using the SQL Query Execution tool. Please make sure you are defining the 'type'
            field in the parameters field of the tool_usage_json.
        """

    connection = SQLDatabaseConnection.objects.get(id=parameters.get("database_connection_id"))
    if not connection:
        return """
            The SQL Database Connection with the ID: " + str(connection_id) + " does not exist in the system.
            Please make sure you are passing a valid database connection ID.
        """

    return None


class ToolExecutor:

    def _execute_sql_query(self, connection_id: int):
        sql_response = None

        sql_connection = SQLDatabaseConnection.objects.get(id=connection_id)
        query_type = self.tool_usage_json.get("parameters").get("type")
        sql_query = self.tool_usage_json.get("parameters").get("sql_query")

        client = InternalSQLClient().get(
            connection=sql_connection
        )

        if query_type == "write":
            sql_response = client.execute_write(
                query=sql_query
            )
        elif query_type == "read":
            sql_response = client.execute_read(
                query=sql_query
            )

        return sql_response

    def __init__(self, assistant: Assistant, tool_usage_json_str: dict):
        self.assistant = assistant
        self.tool_usage_json_str = tool_usage_json_str
        self.tool_usage_json = {}
        try:
            self.tool_usage_json = json.loads(tool_usage_json_str)
        except Exception as e:
            print("Error decoding the JSON: ", e)

    def use_tool(self):
        error = validate_main_tool_json(tool_usage_json=self.tool_usage_json)
        if error: return error

        tool_name = self.tool_usage_json.get("tool")
        tool_response = f"""
            Tool Response: {tool_name}

            '''
        """

        ##################################################
        # SQL Query Execution Tool
        if tool_name == ToolTypeNames.SQL_QUERY_EXECUTION:
            error = validate_sql_query_execution_tool_json(tool_usage_json=self.tool_usage_json)
            if error: return error

            sql_response = self._execute_sql_query(
                connection_id=self.tool_usage_json.get("parameters").get("database_connection_id")
            )
            # Convert the tool response to a string and pretty format
            sql_response_raw_str = json.dumps(sql_response, sort_keys=True, default=str)
            tool_response += sql_response_raw_str
        ##################################################

        ##################################################
        # IF NO TOOL IS FOUND WITH THE GIVEN NAME
        else:
            return """
                There is no tool with the name: " + tool_name + " in the system. Please make sure you are defining
                the correct tool name in the tool_usage_json.
            """
        ##################################################

        tool_response += f"""
            '''
        """

        return tool_response, tool_name
