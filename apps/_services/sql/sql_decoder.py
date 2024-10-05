#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: sql_decoder.py
#  Last Modified: 2024-09-28 22:17:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:33
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: sql_decoder.py
#  Last Modified: 2024-08-05 21:13:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:13:32
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

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
