#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: vector_store_executor.py
#  Last Modified: 2024-12-11 08:11:27
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-11 08:14:36
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

from apps.core.vector_operations.utils import (
    DOCUMENT_SEARCH_QUERY_SET_MAXIMUM_SIZE
)

from apps.datasource_knowledge_base.utils import (
    OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS,
    OpenAIEmbeddingModels
)

logger = logging.getLogger(__name__)

from apps.datasource_knowledge_base.models import (
    DocumentKnowledgeBaseConnection,
    KnowledgeBaseDocument,
    DocumentChunkVectorData,
    VECTOR_INDEX_PATH_KNOWLEDGE_BASE_DOCUMENTS
)


class VectorStoreExecutor:

    def __init__(self, connection_id):
        self.connection_id = connection_id

        self.connection_object = DocumentKnowledgeBaseConnection.objects.get(
            id=connection_id
        )

        if self.connection_object is None:
            logger.error(
                f"Error: Document Storage Connection with ID {connection_id} not found."
            )

        self.document_storage_index_path = os.path.join(
            VECTOR_INDEX_PATH_KNOWLEDGE_BASE_DOCUMENTS,
            f'knowledge_base_storage_index_{self.connection_object.id}.index'
        )

        if os.path.exists(
            self.document_storage_index_path
        ):
            self.document_storage_index = faiss.read_index(
                self.document_storage_index_path
            )

        else:
            self.document_storage_index = faiss.IndexIDMap(
                faiss.IndexFlatL2(
                    OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS
                )
            )

            faiss.write_index(
                self.document_storage_index,
                self.document_storage_index_path
            )

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

    def search_within_document_chunks(
        self,
        document_file_name: str,
        query: str
    ):

        document_items: List[KnowledgeBaseDocument] = self.connection_object.knowledge_base_documents.all()

        existing_file_names = [
            item.document_file_name for item in document_items
        ]

        n_results = int(
            self.connection_object.search_instance_retrieval_limit
        )

        total_vectors = self.document_storage_index.ntotal

        k = min(
            DOCUMENT_SEARCH_QUERY_SET_MAXIMUM_SIZE,
            total_vectors
        )

        query_vector = np.array(
            [
                self._generate_query_embedding(query)
            ],
            dtype=np.float32
        )

        if self.document_storage_index is None:
            raise ValueError("[search_within_document_chunks] FAISS index not initialized or loaded properly.")

        distances, ids = self.document_storage_index.search(
            query_vector,
            k=k
        )

        print(f"Unfiltered results have been found. Total: {len(ids[0])}")

        filtered_results = []

        # Post-filter the results by document file name

        if (
            document_file_name is not None and
            document_file_name != "" and
            document_file_name in existing_file_names
        ):

            for item_id, distance in zip(
                ids[0],
                distances[0]
            ):

                if item_id == -1:
                    continue

                try:
                    instance: DocumentChunkVectorData = DocumentChunkVectorData.objects.get(
                        id=item_id
                    )

                    # Filter by document file name

                    if instance.knowledge_base_document.document_file_name == document_file_name:

                        filtered_results.append(
                            {
                                "id": instance.id,
                                "data": instance.raw_data,
                                "distance": distance,
                            }
                        )

                        if len(filtered_results) >= n_results:
                            break

                except DocumentChunkVectorData.DoesNotExist:
                    logger.error(f"Document Item Chunk Instance with ID {item_id} not found in the database.")

            return filtered_results

        else:

            # Do not filter by document file name

            for item_id, distance in zip(ids[0], distances[0]):

                if item_id == -1:
                    continue

                try:

                    instance = DocumentChunkVectorData.objects.get(
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

                except DocumentChunkVectorData.DoesNotExist:
                    logger.error(f"Document Item Chunk Instance with ID {item_id} not found in the database.")

            return filtered_results
