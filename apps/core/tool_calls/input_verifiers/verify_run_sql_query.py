#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: verify_run_sql_query.py
#  Last Modified: 2024-10-05 02:31:01
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


from apps.datasource_sql.models import SQLDatabaseConnection


def verify_run_sql_query_content(content: dict):
    if "parameters" not in content:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the SQL Query
            Execution tool. Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """
    ps = content.get("parameters")
    if "sql_query" not in ps:
        return """
            The 'sql_query' field is missing from the 'parameters' field in the tool_usage_json. This field is
            mandatory for using the SQL Query Execution tool. Please make sure you are defining the 'sql_query' field
            in the parameters field of the tool_usage_json.
        """
    if "database_connection_id" not in ps:
        return """
            The 'database_connection_id' field is missing from the 'parameters' field in the tool_usage_json. This
            field is mandatory for using the SQL Query Execution tool. Please make sure you are defining the
            'database_connection_id' field in the parameters field of the tool_usage_json.
        """
    if "type" not in ps:
        return """
            The 'type' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the SQL Query Execution tool. This must either be 'read' or 'write' based on the type of query you
            are executing. Please make sure you are defining the 'type' field in the parameters field of the
            tool_usage_json.
        """
    db_operation_type = ps.get("type")
    if db_operation_type not in ["read", "write"]:
        return """
            The 'type' field in the 'parameters' field of the tool_usage_json must either be 'read' or 'write'. This
            field is mandatory for using the SQL Query Execution tool. Please make sure you are defining the 'type'
            field in the parameters field of the tool_usage_json.
        """
    c = SQLDatabaseConnection.objects.get(id=ps.get("database_connection_id"))
    if not c:
        return f"""
            The SQL Database Connection with the ID: {c.id} does not exist in the system.
            Please make sure you are passing a valid database connection ID.
        """
    return None
