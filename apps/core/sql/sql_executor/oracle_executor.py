#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: oracle_executor.py
#  Last Modified: 2024-12-17 18:24:35
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-17 18:24:36
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
import os

from typing import (
    List,
    Dict
)

import faiss
import numpy as np
import oracledb

from apps.core.internal_cost_manager.costs_map import (
    InternalServiceCosts
)

from apps.core.sql.utils import (
    before_execute_sql_query,
    can_write_to_database
)

from apps.datasource_sql.models import (
    SQLDatabaseConnection,
    SQLSchemaChunkVectorData
)

from apps.datasource_sql.utils import (
    DEFAULT_SEARCH_RESULTS_SQL_SCHEMA,
    OpenAIEmbeddingModels,
    VECTOR_INDEX_PATH_SQL_SCHEMAS,
    OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS
)

from apps.llm_transaction.models import LLMTransaction

from apps.llm_transaction.utils import (
    LLMTransactionSourcesTypesNames
)

logger = logging.getLogger(__name__)


class OracleDBExecutor:
    def __init__(self, connection: SQLDatabaseConnection):
        before_execute_sql_query(
            connection
        )

        self.conn_params = {
            'user': connection.username,
            'password': connection.password,
            'dsn': f"{connection.host}:{connection.port}/{connection.database_name}"
        }

        self.connection_object = connection
        self.sql_database_schemas_index_path = os.path.join(
            VECTOR_INDEX_PATH_SQL_SCHEMAS,
            f"sql_schemas_index_{self.connection_object.id}.index"
        )

        if os.path.exists(self.sql_database_schemas_index_path):
            self.sql_database_schemas_index = faiss.read_index(
                self.sql_database_schemas_index_path
            )

        else:
            self.sql_database_schemas_index = faiss.IndexIDMap(
                faiss.IndexFlatL2(
                    OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS
                )
            )

            faiss.write_index(
                self.sql_database_schemas_index,
                self.sql_database_schemas_index_path
            )

    def execute_read(self, query, parameters=None):
        from apps.core.generative_ai.utils import (
            GPT_DEFAULT_ENCODING_ENGINE,
            ChatRoles
        )

        output = {
            "status": True,
            "error": ""
        }

        try:
            with oracledb.connect(**self.conn_params) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, parameters or {})
                    output = cursor.fetchall()

            logger.info("Query executed successfully.")

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

        logger.info("Transaction saved successfully.")

        return output

    def execute_write(self, query, parameters=None):
        from apps.core.generative_ai.utils import (
            GPT_DEFAULT_ENCODING_ENGINE,
            ChatRoles
        )

        if not can_write_to_database(
            self.connection_object
        ):
            return {
                "status": False,
                "error": "No write permission within this database connection."
            }

        output = {
            "status": True,
            "error": ""
        }

        try:
            with oracledb.connect(
                **self.conn_params
            ) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        query,
                        parameters or {}
                    )

                    conn.commit()

            logger.info("Write query executed successfully.")

        except Exception as e:
            output["status"] = False
            output["error"] = str(e)

            logger.error(f"Error occurred while executing write query: {e}")

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

        logger.info("Transaction saved successfully.")

        return output

    def _generate_query_embedding(self, query: str) -> List[float]:
        from apps.core.generative_ai.gpt_openai_manager import (
            OpenAIGPTClientManager
        )

        c = OpenAIGPTClientManager.get_naked_client(
            llm_model=self.connection_object.assistant.llm_model
        )

        response = c.embeddings.create(
            input=query,
            model=OpenAIEmbeddingModels.TEXT_EMBEDDING_3_LARGE
        )

        return response.data[0].embedding

    def search_sql_database_schema(
        self,
        query: str,
        n_results: int = DEFAULT_SEARCH_RESULTS_SQL_SCHEMA
    ) -> List[Dict]:

        query_vector = np.array(
            [
                self._generate_query_embedding(
                    query
                )
            ],
            dtype=np.float32
        )

        if self.sql_database_schemas_index is None:
            raise ValueError(
                "[search_sql_database_schema] FAISS index not initialized or loaded properly."
            )

        distances, ids = self.sql_database_schemas_index.search(
            query_vector,
            n_results
        )

        results = []
        for item_id, distance in zip(
            ids[0],
            distances[0]
        ):
            if item_id == -1:
                continue

            try:
                instance = SQLSchemaChunkVectorData.objects.get(
                    id=item_id
                )

                results.append(
                    {
                        "id": instance.id,
                        "data": instance.raw_data,
                        "distance": distance,
                    }
                )

            except SQLSchemaChunkVectorData.DoesNotExist:
                logger.error(f"SQL Database Schema Chunk Instance with ID {item_id} not found in the vector database.")

        return results
