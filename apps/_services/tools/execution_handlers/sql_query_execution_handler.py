#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: sql_query_execution_handler.py
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#

from apps._services.sql.sql_decoder import InternalSQLClient
from apps.datasource_sql.models import SQLDatabaseConnection


def execute_sql_query(connection_id: int, query_type: str, sql_query: str):
    sql_response = None
    sql_connection = SQLDatabaseConnection.objects.get(id=connection_id)
    print(f"[sql_query_execution_handler.execute_sql_query] Executing the SQL query: {sql_query}.")
    try:
        client = InternalSQLClient().get(
            connection=sql_connection
        )
        if query_type == "write":
            print(f"[sql_query_execution_handler.execute_sql_query] Executing the SQL write query: {sql_query}.")
            sql_response = client.execute_write(query=sql_query)
        elif query_type == "read":
            print(f"[sql_query_execution_handler.execute_sql_query] Executing the SQL read query: {sql_query}.")
            sql_response = client.execute_read(query=sql_query)
    except Exception as e:
        error = f"[sql_query_execution_handler.execute_sql_query] Error occurred while executing the SQL query: {str(e)}"
        return error
    print(f"[sql_query_execution_handler.execute_sql_query] SQL query executed successfully.")
    return sql_response
