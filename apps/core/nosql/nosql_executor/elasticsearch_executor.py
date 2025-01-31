#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: elasticsearch_executor.py
#  Last Modified: 2024-12-17 18:25:28
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-17 18:25:29
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

from elasticsearch import (
    Elasticsearch,
    helpers
)

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
    GPT_DEFAULT_ENCODING_ENGINE
)

from apps.core.generative_ai.utils import (
    ChatRoles
)
from config import settings

logger = logging.getLogger(__name__)


class ElasticSearchNoSQLExecutor:
    def __init__(self, connection: NoSQLDatabaseConnection):
        self.conn_uri = f"{connection.host}"

        self.connection_object = connection

        self.nosql_database_schemas_index_path = os.path.join(
            VECTOR_INDEX_PATH_NOSQL_SCHEMAS,
            f'nosql_schemas_index_{self.connection_object.id}.index'
        )

        self.client = Elasticsearch(
            hosts=[
                {
                    "host": self.connection_object.host,
                    "port": self.connection_object.port,
                    "scheme": (
                        "http" if settings.ENVIRONMENT == 'local' else "https"
                    ),
                }
            ],
            basic_auth=(
                self.connection_object.username,
                self.connection_object.password
            )
        )

        if os.path.exists(self.nosql_database_schemas_index_path):
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

    @staticmethod
    def execute_read__headless(
        assistant,
        connection_params,
        query,
        parameters=None
    ):

        headless_client = Elasticsearch(
            hosts=[
                {
                    "host": connection_params['host'],
                    "port": connection_params['port'],
                    "scheme": (
                        "http" if settings.ENVIRONMENT == 'local' else "https"
                    ),
                }
            ],
            basic_auth=(
                connection_params['username'],
                connection_params['password']
            )
        )

        output = {
            "status": True,
            "error": ""
        }

        try:
            if isinstance(query, list):
                result = headless_client.msearch(
                    body=query
                )

            else:
                result = headless_client.search(
                    index=connection_params['bucket_name'],
                    body=query
                )

            output["result"] = result
            logger.info("Query executed successfully.")

        except Exception as e:
            logger.error(f"Error occurred while executing query: {e}")

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

    def execute_read(self, query):
        output = {
            "status": True,
            "error": ""
        }

        try:
            if isinstance(query, list):
                result = self.client.msearch(
                    body=query
                )

            else:
                result = self.client.search(
                    index=self.connection_object.bucket_name,
                    body=query
                )

            output["result"] = result
            logger.info("Query executed successfully.")

        except Exception as e:
            logger.error(f"Error occurred while executing query: {e}")

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

    def execute_write(self, query):
        output = {
            "status": True,
            "error": ""
        }

        if not can_write_to_database(self.connection_object):
            return {"status": False, "error": "No write permission within this database connection."}

        try:

            result = None

            if isinstance(query, list):
                helpers.bulk(
                    self.client,
                    query
                )

            else:
                result = self.client.index(
                    index=self.connection_object.bucket_name,
                    body=query
                )

            output["result"] = result

            logger.info("Query executed successfully.")

        except Exception as e:
            logger.error(f"Error occurred while executing query: {e}")

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
