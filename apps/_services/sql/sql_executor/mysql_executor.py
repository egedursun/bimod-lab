#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: mysql_executor.py
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
#  File: mysql_executor.py
#  Last Modified: 2024-09-28 15:44:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:12:42
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

import mysql
from mysql.connector import cursor_cext

from apps._services.config.costs_map import ToolCostsMap
from apps._services.sql.utils import before_execute_sql_query, can_write_to_database
from apps.datasource_sql.models import SQLDatabaseConnection
from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import TransactionSourcesNames


class MySQLExecutor:
    def __init__(self, connection: SQLDatabaseConnection):
        ##################################################
        # run the before_execute_sql_query function to refresh the schema
        before_execute_sql_query(connection)
        ##################################################

        self.conn_params = {
            'user': connection.username,
            'password': connection.password,
            'host': connection.host,
            'database': connection.database_name,
            'port': connection.port
        }
        self.connection_object = connection

    def execute_read(self, query, parameters=None):
        from apps._services.llms.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps._services.llms.utils import ChatRoles
        results = {"status": True, "error": ""}
        try:
            with mysql.connector.connect(**self.conn_params) as conn:
                with conn.cursor(cursor_class=cursor_cext.CMySQLCursorDict, buffered=True) as cursor:
                    cursor.execute(query, parameters)
                    results = cursor.fetchall()
            print(f"[MySQLExecutor.execute_read] Read operation is successful.")
        except Exception as e:
            print(f"[PostgresSQLExecutor.execute_read] Error executing MySQL / Read Query: {e}")
            results["status"] = False
            results["error"] = str(e)

        new_transaction = LLMTransaction(
            organization=self.connection_object.assistant.organization,
            model=self.connection_object.assistant.llm_model,
            responsible_user=None,
            responsible_assistant=self.connection_object.assistant,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            llm_cost=ToolCostsMap.SQLReadExecutor.COST,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=TransactionSourcesNames.SQL_READ,
            is_tool_cost=True
        )
        new_transaction.save()
        print(f"[MySQLExecutor.execute_read] Transaction has been saved.")
        return results

    def execute_write(self, query, parameters=None):
        from apps._services.llms.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps._services.llms.utils import ChatRoles
        if not can_write_to_database(self.connection_object):
            return {"status": False, "error": "No write permission within this database connection."}

        output = {"status": True, "error": ""}
        try:
            with mysql.connector.connect(**self.conn_params) as conn:
                with conn.cursor(buffered=True) as cursor:
                    cursor.execute(query, parameters)
                    conn.commit()
            print(f"[MySQLExecutor.execute_write] Write operation is successful.")
        except Exception as e:
            print(f"[PostgresSQLExecutor.execute_write] Error executing MySQL / Write Query: {e}")
            output["status"] = False
            output["error"] = str(e)

        new_transaction = LLMTransaction(
            organization=self.connection_object.assistant.organization,
            model=self.connection_object.assistant.llm_model,
            responsible_user=None,
            responsible_assistant=self.connection_object.assistant,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            llm_cost=ToolCostsMap.SQLWriteExecutor.COST,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=TransactionSourcesNames.SQL_WRITE,
            is_tool_cost=True
        )
        new_transaction.save()
        print(f"[MySQLExecutor.execute_write] Transaction has been saved.")
        return output
