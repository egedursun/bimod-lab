#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: core_service_sql_schema_search.py
#  Last Modified: 2024-12-04 01:31:28
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-04 01:31:31
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

from apps.core.sql.sql_executor import (
    MySQLExecutor,
    PostgresSQLExecutor,
)

from apps.datasource_sql.models import (
    SQLDatabaseConnection
)

from apps.datasource_sql.utils import (
    DBMSChoicesNames
)

logger = logging.getLogger(__name__)


def run_query_search_sql_database_schema(
    connection_id: str,
    query: str
):
    try:
        connection = SQLDatabaseConnection.objects.get(
            id=connection_id
        )

        if not connection:
            return f"Connection with ID: {connection_id} does not exist."

        if connection.dbms_type == DBMSChoicesNames.MYSQL:
            xc = MySQLExecutor(
                connection=connection
            )

        elif connection.dbms_type == DBMSChoicesNames.POSTGRESQL:
            xc = PostgresSQLExecutor(
                connection=connection
            )

        else:
            return f"DBMS Type: {connection.dbms_type} is not supported."

        output = xc.search_sql_database_schema(
            query=query
        )

    except Exception as e:
        logger.error(f"Error occurred while executing the SQL Database Schema Search query: {str(e)}")
        error_msg = f"Error occurred while executing the SQL Database Schema Search query: {str(e)}"

        return error_msg

    return output
