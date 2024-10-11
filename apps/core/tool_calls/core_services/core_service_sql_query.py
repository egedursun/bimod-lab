#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: core_service_sql_query.py
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


from apps.core.sql.sql_decoder import InternalSQLClient
from apps.datasource_sql.models import SQLDatabaseConnection


def run_sql_query(c_id: int, sql_query_type: str, query_content: str):
    sql_response = None
    sql_connection = SQLDatabaseConnection.objects.get(id=c_id)
    try:
        client = InternalSQLClient().get(
            connection=sql_connection
        )
        if sql_query_type == "write":
            sql_response = client.execute_write(query=query_content)
        elif sql_query_type == "read":
            sql_response = client.execute_read(query=query_content)
    except Exception as e:
        error_msg = f"Error occurred while executing the SQL query: {str(e)}"
        return error_msg
    return sql_response
