#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: mysql_executor.py
#  Last Modified: 2024-10-05 02:25:59
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
#
#
import logging

import mysql
from mysql.connector import cursor_cext

from apps.core.internal_cost_manager.costs_map import InternalServiceCosts
from apps.core.sql.utils import before_execute_sql_query, can_write_to_database
from apps.datasource_sql.models import SQLDatabaseConnection
from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import LLMTransactionSourcesTypesNames


logger = logging.getLogger(__name__)


class MySQLExecutor:
    def __init__(
        self,
        connection: SQLDatabaseConnection
    ):
        before_execute_sql_query(connection)
        self.conn_params = {
            'user': connection.username,
            'password': connection.password,
            'host': connection.host,
            'database': connection.database_name,
            'port': connection.port
        }
        self.connection_object = connection

    def execute_read(
        self,
        query,
        parameters=None
    ):

        from apps.core.generative_ai.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps.core.generative_ai.utils import ChatRoles

        output = {
            "status": True,
            "error": ""
        }

        try:
            with mysql.connector.connect(**self.conn_params) as conn:
                with conn.cursor(
                    cursor_class=cursor_cext.CMySQLCursorDict,
                    buffered=True
                ) as cursor:

                    cursor.execute(
                        query,
                        parameters
                    )

                    output = cursor.fetchall()

            logger.info(f"Query executed successfully.")

        except Exception as e:
            output["status"] = False
            output["error"] = str(e)
            logger.error(f"Error occurred while executing query: {e}")

        new_tx = LLMTransaction(
            organization=self.connection_object.assistant.organization,
            model=self.connection_object.assistant.llm_model,
            responsible_user=None,
            responsible_assistant=self.connection_object.assistant,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            llm_cost=InternalServiceCosts.SQLReadExecutor.COST,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=LLMTransactionSourcesTypesNames.SQL_READ,
            is_tool_cost=True
        )
        new_tx.save()

        logger.info(f"Transaction saved successfully.")
        return output

    def execute_write(
        self,
        query,
        parameters=None
    ):

        from apps.core.generative_ai.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps.core.generative_ai.utils import ChatRoles

        if not can_write_to_database(self.connection_object):

            return {
                "status": False,
                "error": "No write permission within this database connection."
            }

        output = {
            "status": True,
            "error": ""
        }

        try:
            with mysql.connector.connect(**self.conn_params) as conn:

                with conn.cursor(buffered=True) as cursor:
                    cursor.execute(
                        query,
                        parameters
                    )
                    conn.commit()

            logger.info(f"Query executed successfully.")

        except Exception as e:
            output["status"] = False
            output["error"] = str(e)
            logger.error(f"Error occurred while executing query: {e}")

        new_tx = LLMTransaction(
            organization=self.connection_object.assistant.organization,
            model=self.connection_object.assistant.llm_model,
            responsible_user=None,
            responsible_assistant=self.connection_object.assistant,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            llm_cost=InternalServiceCosts.SQLWriteExecutor.COST,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=LLMTransactionSourcesTypesNames.SQL_WRITE,
            is_tool_cost=True
        )
        new_tx.save()

        logger.info(f"Transaction saved successfully.")
        return output
