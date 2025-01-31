#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: neo4j_executor.py
#  Last Modified: 2024-12-17 18:25:39
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-17 18:25:40
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

from neo4j import GraphDatabase

from apps.datasource_nosql.models import (
    NoSQLDatabaseConnection
)

from apps.llm_transaction.models import (
    LLMTransaction
)

from apps.core.nosql.utils import (
    can_write_to_database
)

from apps.core.internal_cost_manager.costs_map import (
    InternalServiceCosts
)

from apps.llm_transaction.utils import (
    LLMTransactionSourcesTypesNames
)

from apps.core.generative_ai.utils import (
    GPT_DEFAULT_ENCODING_ENGINE,
    ChatRoles
)

logger = logging.getLogger(__name__)


class Neo4JNoSQLExecutor:
    def __init__(self, connection: NoSQLDatabaseConnection):
        self.connection_object = connection

        self.driver = GraphDatabase.driver(
            uri=f"bolt://{connection.host}:{connection.port}",
            auth=(
                connection.username,
                connection.password
            )
        )

    @staticmethod
    def execute_read__headless(
        assistant,
        connection_params,
        query,
        parameters=None
    ):

        headless_driver = GraphDatabase.driver(
            uri=f"bolt://{connection_params["host"]}:{connection_params["port"]}",
            auth=(
                connection_params["username"],
                connection_params["password"]
            )
        )

        output = {
            "status": True,
            "error": ""
        }

        try:
            with headless_driver.session() as session:
                result = session.run(
                    query
                )

                output["result"] = [
                    record.data() for record in result
                ]

                logger.info("Read query executed successfully.")

        except Exception as e:
            logger.error(f"Error occurred while executing read query: {e}")

            output["status"] = False
            output["error"] = str(e)

        new_tx = LLMTransaction(
            organization=assistant.organization,
            model=assistant.llm_model,
            responsible_user=None,
            responsible_assistant=assistant,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            llm_cost=InternalServiceCosts.NoSQLReadExecutor.COST,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=LLMTransactionSourcesTypesNames.NOSQL_READ,
            is_tool_cost=True
        )

        new_tx.save()

        logger.info("Transaction saved successfully.")

        return output

    def execute_read(self, query: str):
        output = {
            "status": True,
            "error": ""
        }

        try:
            with self.driver.session() as session:
                result = session.run(
                    query
                )

                output["result"] = [
                    record.data() for record in result
                ]

                logger.info("Read query executed successfully.")

        except Exception as e:
            logger.error(f"Error occurred while executing read query: {e}")

            output["status"] = False
            output["error"] = str(e)

        new_tx = LLMTransaction(
            organization=self.connection_object.assistant.organization,
            model=self.connection_object.assistant.llm_model,
            responsible_user=None,
            responsible_assistant=self.connection_object.assistant,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            llm_cost=InternalServiceCosts.NoSQLReadExecutor.COST,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=LLMTransactionSourcesTypesNames.NOSQL_READ,
            is_tool_cost=True
        )

        new_tx.save()

        logger.info("Transaction saved successfully.")

        return output

    def execute_write(self, query: str):
        output = {
            "status": True,
            "error": ""
        }

        if not can_write_to_database(
            self.connection_object
        ):
            return {
                "status": False,
                "error": "No write permission within this database connection."
            }

        try:
            with self.driver.session() as session:
                session.run(
                    query
                )

                logger.info("Write query executed successfully.")

        except Exception as e:
            logger.error(f"Error occurred while executing write query: {e}")

            output["status"] = False
            output["error"] = str(e)

        new_tx = LLMTransaction(
            organization=self.connection_object.assistant.organization,
            model=self.connection_object.assistant.llm_model,
            responsible_user=None,
            responsible_assistant=self.connection_object.assistant,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            llm_cost=InternalServiceCosts.NoSQLWriteExecutor.COST,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=LLMTransactionSourcesTypesNames.NOSQL_WRITE,
            is_tool_cost=True
        )

        new_tx.save()

        logger.info("Transaction saved successfully.")

        return output

    def close(self):
        self.driver.close()

        logger.info("Neo4j connection closed.")
