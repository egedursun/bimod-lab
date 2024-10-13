#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#


from apps.core.sql.sql_executor import PostgresSQLExecutor, MySQLExecutor
from apps.core.sql.utils import SQL_DBMS_PROVIDERS
from apps.datasource_sql.models import SQLDatabaseConnection


class InternalSQLClient:
    @staticmethod
    def get(connection: SQLDatabaseConnection):
        if connection.dbms_type == SQL_DBMS_PROVIDERS["POSTGRESQL"]["code"]:
            return PostgresSQLExecutor(connection)
        elif connection.dbms_type == SQL_DBMS_PROVIDERS["MYSQL"]["code"]:
            return MySQLExecutor(connection)
