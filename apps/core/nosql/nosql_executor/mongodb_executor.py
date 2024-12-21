#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: mongodb_executor.py
#  Last Modified: 2024-12-18 10:30:37
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-18 10:46:18
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
import json
import logging
import os

from typing import (
    List,
    Dict
)

from pymongo import (
    MongoClient
)
from pymongo.errors import (
    PyMongoError
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

logger = logging.getLogger(__name__)


class MongoDBNoSQLExecutor:
    def __init__(self, connection: NoSQLDatabaseConnection):
        # Currently, it's costly to run schema retrieval every time a query is executed.
        # before_execute_nosql_query(connection)

        self.database_name = connection.bucket_name.split(".")[0]
        self.collection_name = connection.bucket_name.split(".")[1]

        self.conn_uri = f"mongodb+srv://{connection.username}:{connection.password}@{connection.host}/{self.database_name}"

        self.connection_object = connection

        self.nosql_database_schemas_index_path = os.path.join(
            VECTOR_INDEX_PATH_NOSQL_SCHEMAS,
            f'nosql_schemas_index_{self.connection_object.id}.index'
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

    def execute_read(self, query):
        output = {
            "status": True,
            "error": ""
        }

        try:
            if isinstance(query, str):
                query = json.loads(query)

        except Exception as e:
            output["status"] = False
            output["error"] = f"Error parsing query: {e}"

            return output

        try:
            client = MongoClient(self.conn_uri)
            db = client[self.database_name]

            if isinstance(
                query,
                list
            ):
                result = db.command(
                    {
                        "aggregate": self.collection_name,
                        "pipeline": query,
                    }
                )

            else:
                result = db.command(query)

            output["result"] = result
            logger.info(f"Query executed successfully.")

        except PyMongoError as e:
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

        logger.info(f"Transaction saved successfully.")

        return output

    def execute_write(self, query):
        output = {
            "status": True,
            "error": ""
        }

        try:
            if isinstance(query, str):
                query = json.loads(query)

        except Exception as e:
            output["status"] = False
            output["error"] = f"Error parsing query: {e}"

            return output

        if not can_write_to_database(
            self.connection_object
        ):
            return {
                "status": False,
                "error": "No write permission within this database connection."
            }

        try:
            client = MongoClient(
                self.conn_uri
            )

            db = client[self.database_name]

            if isinstance(
                query,
                list
            ):
                result = db.command(
                    {
                        "aggregate": self.collection_name,
                        "pipeline": query,
                    }
                )

            else:
                result = db.command(query)

            output["result"] = result

            logger.info(f"Query executed successfully.")

        except PyMongoError as e:
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

        logger.info(f"Transaction saved successfully.")

        return output

    def _generate_query_embedding(
        self,
        query: str
    ) -> List[float]:

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
                self._generate_query_embedding(query)
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

        for item_id, distance in zip(ids[0], distances[0]):

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
                        "distance": distance,
                    }
                )

            except NoSQLSchemaChunkVectorData.DoesNotExist:
                logger.error(
                    f"NoSQL Database Schema Chunk Instance with ID {item_id} not found in the vector database."
                )

        return results
