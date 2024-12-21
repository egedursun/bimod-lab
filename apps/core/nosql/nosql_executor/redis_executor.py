#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: redis_executor.py
#  Last Modified: 2024-12-17 18:25:15
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-17 18:25:15
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
    Dict,
    Any
)

import redis
import faiss
import numpy as np

from apps.core.internal_cost_manager.costs_map import (
    InternalServiceCosts
)

from apps.core.nosql.utils import (
    can_write_to_database
)

from apps.datasource_nosql.models import (
    NoSQLDatabaseConnection,
    NoSQLSchemaChunkVectorData
)

from apps.datasource_nosql.utils import (
    OpenAIEmbeddingModels,
    DEFAULT_SEARCH_RESULTS_NOSQL_SCHEMA,
    VECTOR_INDEX_PATH_NOSQL_SCHEMAS,
    OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS
)

from apps.llm_transaction.models import (
    LLMTransaction
)

from apps.llm_transaction.utils import (
    LLMTransactionSourcesTypesNames
)

from apps.core.generative_ai.utils import (
    GPT_DEFAULT_ENCODING_ENGINE,
    ChatRoles
)

logger = logging.getLogger(__name__)


class RedisNoSQLExecutor:
    def __init__(self, connection: NoSQLDatabaseConnection):
        connection_params = {
            'host': connection.host,
            'port': connection.port,
            'socket_timeout': 10
        }

        if connection.password and connection.password != '':
            connection_params['password'] = connection.password

        if connection.username and connection.username != '':
            connection_params['username'] = connection.username

        self.connection_object = connection

        self.nosql_database_schemas_index_path = os.path.join(
            VECTOR_INDEX_PATH_NOSQL_SCHEMAS,
            f'nosql_schemas_index_{self.connection_object.id}.index')

        if os.path.exists(
            self.nosql_database_schemas_index_path
        ):
            self.nosql_database_schemas_index = faiss.read_index(
                self.nosql_database_schemas_index_path
            )

        else:
            self.nosql_database_schemas_index = faiss.IndexIDMap(
                faiss.IndexFlatL2(
                    OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS
                )
            )

            faiss.write_index(
                self.nosql_database_schemas_index,
                self.nosql_database_schemas_index_path
            )

        self.redis_client = redis.StrictRedis(
            **connection_params
        )

    def execute_read(self, query: str, parameters: Any = None):
        output = {
            "status": True,
            "error": ""
        }

        try:
            logger.info(f"Executing query: {query}")

            result = self.redis_client.execute_command(
                query,
                *parameters
            ) if parameters else self.redis_client.execute_command(
                query
            )

            output["result"] = result

            logger.info(f"Query executed successfully.")

        except Exception as e:
            logger.error(f"Error occurred while executing query: {e}")

            output["status"] = False
            output["error"] = str(e)

        self._log_transaction(
            InternalServiceCosts.NoSQLReadExecutor.COST,
            LLMTransactionSourcesTypesNames.NOSQL_READ
        )

        return output

    def execute_write(self, query: str, parameters: Any = None):
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
            logger.info(f"Executing query: {query}")

            result = self.redis_client.execute_command(
                query,
                *parameters
            ) if parameters else self.redis_client.execute_command(
                query
            )

            output["result"] = result

            logger.info(f"Query executed successfully.")

        except Exception as e:
            logger.error(f"Error occurred while executing query: {e}")

            output["status"] = False
            output["error"] = str(e)

        self._log_transaction(
            InternalServiceCosts.NoSQLWriteExecutor.COST,
            LLMTransactionSourcesTypesNames.NOSQL_WRITE
        )

        return output

    def _generate_query_embedding(self, query: str) -> List[float]:
        from apps.core.generative_ai.gpt_openai_manager import (
            OpenAIGPTClientManager
        )

        client = OpenAIGPTClientManager.get_naked_client(
            llm_model=self.connection_object.assistant.llm_model
        )

        response = client.embeddings.create(
            input=query,
            model=OpenAIEmbeddingModels.TEXT_EMBEDDING_3_LARGE
        )

        return response.data[0].embedding

    def search_nosql_database_schema(
        self,
        query: str,
        n_results: int = DEFAULT_SEARCH_RESULTS_NOSQL_SCHEMA
    ) -> List[Dict]:
        query_vector = np.array(
            [
                self._generate_query_embedding(
                    query
                )
            ],
            dtype=np.float32
        )

        if self.nosql_database_schemas_index is None:
            raise ValueError("[search_nosql_database_schema] FAISS index not initialized or loaded properly.")

        distances, ids = self.nosql_database_schemas_index.search(
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
                instance = NoSQLSchemaChunkVectorData.objects.get(
                    id=item_id
                )

                results.append(
                    {
                        "id": instance.id,
                        "data": instance.raw_data,
                        "distance": distance
                    }
                )

            except NoSQLSchemaChunkVectorData.DoesNotExist:
                logger.error(
                    f"NoSQL Database Schema Chunk Instance with ID {item_id} not found in the vector database."
                )

        return results

    def _log_transaction(
        self,
        cost: float,
        source: str
    ):
        new_tx = LLMTransaction(
            organization=self.connection_object.assistant.organization,
            model=self.connection_object.assistant.llm_model,
            responsible_user=None,
            responsible_assistant=self.connection_object.assistant,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            llm_cost=cost,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=source,
            is_tool_cost=True
        )

        new_tx.save()

        logger.info(f"Transaction saved successfully.")
