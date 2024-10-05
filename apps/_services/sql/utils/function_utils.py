#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: function_utils.py
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
#  File: function_utils.py
#  Last Modified: 2024-09-28 00:42:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:13:27
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from apps.datasource_sql.models import SQLDatabaseConnection
from apps.datasource_sql.utils import DBMSChoicesNames


def before_execute_sql_query(connection: SQLDatabaseConnection):
    # This function is called before executing the SQL query, to refresh the database schema
    old_schema_json = connection.schema_data_json
    new_schema = {}
    if connection.dbms_type == DBMSChoicesNames.POSTGRESQL:
        new_schema = connection.retrieve_postgresql_schema()
    elif connection.dbms_type == DBMSChoicesNames.MYSQL:
        new_schema = connection.retrieve_mysql_schema()
    if new_schema != old_schema_json:
        connection.schema_data_json = new_schema
        connection.save()


def can_write_to_database(connection: SQLDatabaseConnection):
    print(f"[sql_executor.can_write_to_database] Checking the write permission for the connection.")
    return not connection.is_read_only
