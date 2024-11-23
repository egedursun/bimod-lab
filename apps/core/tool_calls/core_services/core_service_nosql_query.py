#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: core_service_nosql_query.py
#  Last Modified: 2024-10-12 17:42:05
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-12 17:42:07
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

from apps.core.nosql.nosql_decoder import InternalNoSQLClient
from apps.datasource_nosql.models import NoSQLDatabaseConnection
from apps.datasource_nosql.utils import NoSQLOperationTypesNames


logger = logging.getLogger(__name__)


def run_nosql_query(
    c_id: int,
    nosql_query_type: str,
    query_content: str
):

    nosql_response = None
    nosql_connection = NoSQLDatabaseConnection.objects.get(
        id=c_id
    )

    try:

        client = InternalNoSQLClient().get(
            connection=nosql_connection
        )

        if nosql_query_type == NoSQLOperationTypesNames.WRITE:

            logger.info(f"Executing NoSQL write query: {query_content}")
            nosql_response = client.execute_write(
                query=query_content
            )

        elif nosql_query_type == NoSQLOperationTypesNames.READ:

            logger.info(f"Executing NoSQL read query: {query_content}")
            nosql_response = client.execute_read(
                query=query_content
            )

    except Exception as e:
        logger.error(f"Error occurred while executing the NoSQL query: {e}")
        error_msg = f"Error occurred while executing the NoSQL query: {str(e)}"
        return error_msg

    logger.info(f"NoSQL query execution output: {nosql_response}")
    return nosql_response
