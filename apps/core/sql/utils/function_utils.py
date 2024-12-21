#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: function_utils.py
#  Last Modified: 2024-10-05 02:26:00
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:34
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

from apps.datasource_sql.models import (
    SQLDatabaseConnection
)

from apps.datasource_sql.utils import (
    DBMSChoicesNames
)

logger = logging.getLogger(__name__)


def before_execute_sql_query(
    connection: SQLDatabaseConnection
):
    logger.info(f"Retrieving schema for connection: {connection.name}")

    old_schema_json = connection.schema_data_json

    new_schema = {}

    if connection.dbms_type == DBMSChoicesNames.POSTGRESQL:
        new_schema = connection.retrieve_postgresql_schema()

    elif connection.dbms_type == DBMSChoicesNames.MYSQL:
        new_schema = connection.retrieve_mysql_schema()

    elif connection.dbms_type == DBMSChoicesNames.MSSQL:
        new_schema = connection.retrieve_mssql_schema()

    elif connection.dbms_type == DBMSChoicesNames.ORACLE:
        new_schema = connection.retrieve_oracle_schema()

    elif connection.dbms_type == DBMSChoicesNames.MARIADB:
        new_schema = connection.retrieve_mariadb_schema()

    if new_schema != old_schema_json:
        connection.schema_data_json = new_schema

        connection.save()


def can_write_to_database(
    connection: SQLDatabaseConnection
):
    logger.info(f"Checking if the connection is read-only: {connection.name}")

    return not connection.is_read_only
