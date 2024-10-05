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


from apps._services.sql.sql_executor import PostgresSQLExecutor, MySQLExecutor
from apps.datasource_sql.models import SQLDatabaseConnection


class InternalSQLClient:
    SQL_DBMS_PROVIDERS = {
        "POSTGRESQL": {"code": "postgresql", "name": "PostgreSQL"},
        "MYSQL": {"code": "mysql", "name": "MySQL"},
    }

    @staticmethod
    def get(connection: SQLDatabaseConnection):
        if connection.dbms_type == InternalSQLClient.SQL_DBMS_PROVIDERS["POSTGRESQL"]["code"]:
            print(f"[InternalSQLClient.get] PostgreSQL connection detected.")
            return PostgresSQLExecutor(connection)
        elif connection.dbms_type == InternalSQLClient.SQL_DBMS_PROVIDERS["MYSQL"]["code"]:
            print(f"[InternalSQLClient.get] MySQL connection detected.")
            return MySQLExecutor(connection)
