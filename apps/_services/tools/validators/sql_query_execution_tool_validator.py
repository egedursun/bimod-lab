#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: sql_query_execution_tool_validator.py
#  Last Modified: 2024-09-28 22:17:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:33
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: sql_query_execution_tool_validator.py
#  Last Modified: 2024-08-05 21:13:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:16:12
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from apps.datasource_sql.models import SQLDatabaseConnection


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
        return f"""
            The SQL Database Connection with the ID: {connection.id} does not exist in the system.
            Please make sure you are passing a valid database connection ID.
        """
    print(f"[sql_query_execution_tool_validator.validate_sql_query_execution_tool_json] Validation is successful.")
    return None
