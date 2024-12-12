#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: codebase_executor.py
#  Last Modified: 2024-10-05 02:20:19
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:36
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
from typing import List

import faiss
import numpy as np

from apps.core.codebase.utils import (
    CODE_BASE_SEARCH_QUERY_SET_MAXIMUM_SIZE
)

from apps.datasource_codebase.models import (
    CodeRepositoryStorageConnection,
    CodeBaseRepository,
    CodeBaseRepositoryChunk,
)

from apps.datasource_codebase.utils import (
    VECTOR_INDEX_PATH_CODEBASE_REPOSITORIES,
    OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS,
    OpenAIEmbeddingModels
)

logger = logging.getLogger(__name__)


class CodeRepositoryExecutor:

    def __init__(self, connection_id):
        self.connection_id = connection_id

        self.connection_object = CodeRepositoryStorageConnection.objects.get(
            id=connection_id
        )

        if self.connection_object is None:
            logger.error(
                f"Error: Code Base Storage Connection with ID {connection_id} not found."
            )

        self.code_base_storage_index_path = os.path.join(
            VECTOR_INDEX_PATH_CODEBASE_REPOSITORIES,
            f'codebase_storage_index_{self.connection_object.id}.index'
        )

        if os.path.exists(
            self.code_base_storage_index_path
        ):
            self.code_base_storage_index = faiss.read_index(
                self.code_base_storage_index_path
            )

        else:
            self.code_base_storage_index = faiss.IndexIDMap(
                faiss.IndexFlatL2(
                    OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS
                )
            )

            faiss.write_index(
                self.code_base_storage_index,
                self.code_base_storage_index_path
            )

    def search_within_code_chunks(
        self,
        repository_uri: str,
        query: str
    ):

        code_base_items: List[CodeBaseRepository] = self.connection_object.code_base_repositories.all()

        existing_repository_uris = [
            item.repository_uri for item in code_base_items
        ]

        n_results = int(
            self.connection_object.search_instance_retrieval_limit
        )

        total_vectors = self.code_base_storage_index.ntotal

        k = min(
            CODE_BASE_SEARCH_QUERY_SET_MAXIMUM_SIZE,
            total_vectors
        )

        query_vector = np.array(
            [
                self._generate_query_embedding(query)
            ],
            dtype=np.float32
        )

        if self.code_base_storage_index is None:
            raise ValueError("FAISS index not initialized or loaded properly.")

        distances, ids = self.code_base_storage_index.search(
            query_vector,
            k=k
        )

        print(f"Unfiltered results have been found. Total: {len(ids[0])}")

        filtered_results = []

        # Post-filter the results by code base repository URI

        if (
            repository_uri is not None and
            repository_uri != "" and
            repository_uri in existing_repository_uris
        ):

            for item_id, distance in zip(
                ids[0],
                distances[0]
            ):

                if item_id == -1:
                    continue

                try:
                    instance: CodeBaseRepositoryChunk = CodeBaseRepositoryChunk.objects.get(
                        id=item_id
                    )

                    # Filter by repository URI

                    if instance.repository_item.repository_uri == repository_uri:

                        filtered_results.append(
                            {
                                "id": instance.id,
                                "data": instance.raw_data,
                                "distance": distance,
                            }
                        )

                        if len(filtered_results) >= n_results:
                            break

                except CodeBaseRepositoryChunk.DoesNotExist:
                    logger.error(f"Code Base Repository Chunk Instance with ID {item_id} not found in the database.")

            return filtered_results

        else:

            # Do not filter by repository URI

            for item_id, distance in zip(ids[0], distances[0]):

                if item_id == -1:
                    continue

                try:

                    instance = CodeBaseRepositoryChunk.objects.get(
                        id=item_id
                    )

                    filtered_results.append(
                        {
                            "id": instance.id,
                            "data": instance.raw_data,
                            "distance": distance,
                        }
                    )

                    if len(filtered_results) >= n_results:
                        break

                except CodeBaseRepositoryChunk.DoesNotExist:
                    logger.error(f"Code Base Repository Chunk Instance with ID {item_id} not found in the database.")

            return filtered_results

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
