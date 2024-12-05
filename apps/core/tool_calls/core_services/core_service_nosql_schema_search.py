#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: core_service_nosql_schema_search.py
#  Last Modified: 2024-12-04 01:31:41
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-04 01:31:41
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

from apps.core.nosql.nosql_executor import CouchbaseNoSQLExecutor
from apps.datasource_nosql.models import NoSQLDatabaseConnection
from apps.datasource_nosql.utils import NoSQLDatabaseChoicesNames

logger = logging.getLogger(__name__)


def run_query_search_nosql_database_schema(
    connection_id: str,
    query: str
):
    try:
        connection = NoSQLDatabaseConnection.objects.get(id=connection_id)
        if not connection:
            return f"Connection with ID: {connection_id} does not exist."

        if connection.nosql_db_type == NoSQLDatabaseChoicesNames.COUCHBASE:
            xc = CouchbaseNoSQLExecutor(
                connection=connection
            )

        else:
            return f"NoSQL Database Type: {connection.nosql_db_type} is not supported."

        output = xc.search_nosql_database_schema(
            query=query
        )

    except Exception as e:
        logger.error(f"Error occurred while executing the NoSQL Database Schema Search query: {str(e)}")
        error_msg = f"Error occurred while executing the NoSQL Database Schema Search query: {str(e)}"
        return error_msg

    return output
