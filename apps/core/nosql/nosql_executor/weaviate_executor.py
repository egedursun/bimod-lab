#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: weaviate_executor.py
#  Last Modified: 2024-12-17 19:50:24
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-17 19:50:26
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
)

import faiss
import numpy as np
import requests

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


class WeaviateNoSQLExecutor:
    def __init__(self, connection: NoSQLDatabaseConnection):
        self.connection = connection
        self.endpoint = connection.host
        self.api_key = connection.password

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        self.nosql_database_schemas_index_path = os.path.join(
            VECTOR_INDEX_PATH_NOSQL_SCHEMAS,
            f'nosql_schemas_index_{self.connection.id}.index'
        )

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

    def _send_graphql_query(
        self,
        query: str,
        variables: Dict = None
    ) -> Dict:
        try:
            logger.info(f"Executing GraphQL query: {query}")

            response = requests.post(
                url=f"{self.endpoint}/v1/graphql",
                headers=self.headers,
                json={
                    "query": query,
                    "variables": variables or {}
                }
            )

            response.raise_for_status()

            return response.json()

        except requests.RequestException as e:
            logger.error(f"GraphQL query failed: {e}")

            return {
                "errors": [str(e)]
            }

    @staticmethod
    def execute_read__headless(
        assistant,
        connection_params,
        query,
        parameters=None
    ):

        headless_headers = {
            "Authorization": f"Bearer {connection_params['password']}",
            "Content-Type": "application/json"
        }

        output = {
            "status": True,
            "error": ""
        }

        try:
            try:
                logger.info(f"Executing GraphQL query: {query}")

                response = requests.post(
                    url=f"{connection_params["host"]}/v1/graphql",
                    headers=headless_headers,
                    json={
                        "query": query,
                        "variables": {}
                    }
                )

                response.raise_for_status()

                result = response.json()

            except requests.RequestException as e:
                logger.error(f"GraphQL query failed: {e}")

                return {
                    "errors": [str(e)]
                }

            if "errors" in result:
                logger.error(f"GraphQL query errors: {result['errors']}")

                output["status"] = False
                output["error"] = result["errors"]

            else:
                output["result"] = result["data"]

                logger.info(f"Query executed successfully.")

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

        logger.info(f"Transaction saved successfully.")

        return output


    def execute_read(self, query: str) -> dict:
        output = {
            "status": True,
            "error": ""
        }

        try:
            result = self._send_graphql_query(
                query
            )

            if "errors" in result:
                logger.error(f"GraphQL query errors: {result['errors']}")

                output["status"] = False
                output["error"] = result["errors"]

            else:
                output["result"] = result["data"]

                logger.info(f"Query executed successfully.")

        except Exception as e:
            logger.error(f"Error occurred while executing query: {e}")

            output["status"] = False
            output["error"] = str(e)

        new_tx = LLMTransaction(
            organization=self.connection.assistant.organization,
            model=self.connection.assistant.llm_model,
            responsible_user=None,
            responsible_assistant=self.connection.assistant,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            llm_cost=InternalServiceCosts.NoSQLReadExecutor.COST,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=LLMTransactionSourcesTypesNames.NOSQL_READ,
            is_tool_cost=True
        )

        new_tx.save()

        logger.info(f"Transaction saved successfully.")

        return output

    def execute_write(self, query: str) -> dict:
        if not can_write_to_database(
            self.connection
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
            result = self._send_graphql_query(
                query
            )

            if "errors" in result:
                logger.error(f"GraphQL query errors: {result['errors']}")

                output["status"] = False
                output["error"] = result["errors"]

            else:
                logger.info(f"Write query executed successfully.")

        except Exception as e:
            logger.error(f"Error occurred while executing query: {e}")

            output["status"] = False
            output["error"] = str(e)

        new_tx = LLMTransaction(
            organization=self.connection.assistant.organization,
            model=self.connection.assistant.llm_model,
            responsible_user=None,
            responsible_assistant=self.connection.assistant,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            llm_cost=InternalServiceCosts.NoSQLWriteExecutor.COST,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=LLMTransactionSourcesTypesNames.NOSQL_WRITE,
            is_tool_cost=True
        )

        new_tx.save()

        logger.info(f"Transaction saved successfully.")

        return output

    def _generate_query_embedding(self, query: str) -> List[float]:
        from apps.core.generative_ai.gpt_openai_manager import (
            OpenAIGPTClientManager
        )

        client = OpenAIGPTClientManager.get_naked_client(
            llm_model=self.connection.assistant.llm_model
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
