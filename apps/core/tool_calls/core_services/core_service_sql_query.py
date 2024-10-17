#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#
import logging

from apps.core.sql.sql_decoder import InternalSQLClient
from apps.datasource_sql.models import SQLDatabaseConnection
from apps.datasource_sql.utils import SQLOperationTypesNames

logger = logging.getLogger(__name__)


def run_sql_query(c_id: int, sql_query_type: str, query_content: str):
    sql_response = None
    sql_connection = SQLDatabaseConnection.objects.get(id=c_id)
    try:
        client = InternalSQLClient().get(
            connection=sql_connection
        )
        if sql_query_type == SQLOperationTypesNames.WRITE:
            logger.info(f"Executing SQL write query: {query_content}")
            sql_response = client.execute_write(query=query_content)
        elif sql_query_type == SQLOperationTypesNames.READ:
            logger.info(f"Executing SQL read query: {query_content}")
            sql_response = client.execute_read(query=query_content)
    except Exception as e:
        logger.error(f"Error occurred while executing the SQL query: {e}")
        error_msg = f"Error occurred while executing the SQL query: {str(e)}"
        return error_msg
    logger.info(f"SQL query execution output: {sql_response}")
    return sql_response
