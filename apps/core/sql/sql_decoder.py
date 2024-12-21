#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: sql_decoder.py
#  Last Modified: 2024-10-05 02:26:00
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

from apps.core.sql.sql_executor import (
    PostgresSQLExecutor,
    MySQLExecutor,
    MSSQLExecutor,
    MariaDBExecutor,
    OracleDBExecutor,
)

from apps.core.sql.utils import (
    SQL_DBMS_PROVIDERS
)

from apps.datasource_sql.models import (
    SQLDatabaseConnection
)

logger = logging.getLogger(__name__)


class InternalSQLClient:
    @staticmethod
    def get(
        connection: SQLDatabaseConnection
    ):

        if connection.dbms_type == SQL_DBMS_PROVIDERS["POSTGRESQL"]["code"]:
            logger.info(f"Creating PostgresSQLExecutor for connection: {connection.name}")

            return PostgresSQLExecutor(
                connection
            )

        elif connection.dbms_type == SQL_DBMS_PROVIDERS["MYSQL"]["code"]:
            logger.info(f"Creating MySQLExecutor for connection: {connection.name}")

            return MySQLExecutor(
                connection
            )

        elif connection.dbms_type == SQL_DBMS_PROVIDERS["MSSQL"]["code"]:
            logger.info(f"Creating MSSQLExecutor for connection: {connection.name}")

            return MSSQLExecutor(
                connection
            )

        elif connection.dbms_type == SQL_DBMS_PROVIDERS["MARIADB"]["code"]:
            logger.info(f"Creating MariaDBExecutor for connection: {connection.name}")

            return MariaDBExecutor(
                connection
            )

        elif connection.dbms_type == SQL_DBMS_PROVIDERS["ORACLE"]["code"]:
            logger.info(f"Creating OracleDBExecutor for connection: {connection.name}")

            return OracleDBExecutor(
                connection
            )
