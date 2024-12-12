#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: website_executor.py
#  Last Modified: 2024-12-07 19:16:16
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-07 19:16:17
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

from apps.core.website.utils import (
    WEBSITE_SEARCH_QUERY_SET_MAXIMUM_SIZE
)

from apps.datasource_website.models import (
    DataSourceWebsiteStorageConnection,
    WebsiteItemChunkVectorData
)

from apps.datasource_website.utils import (
    OpenAIEmbeddingModels,
    VECTOR_INDEX_PATH_WEBSITE_ITEMS,
    OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS
)

logger = logging.getLogger(__name__)


class WebsiteExecutionManager:

    def __init__(self, connection_id):
        self.connection_id = connection_id

        self.connection_object = DataSourceWebsiteStorageConnection.objects.get(
            id=connection_id
        )

        if self.connection_object is None:
            logger.error(
                f"Error: Website Connection with ID {connection_id} not found."
            )

        self.website_storage_schemas_index_path = os.path.join(
            VECTOR_INDEX_PATH_WEBSITE_ITEMS,
            f'website_storage_index_{self.connection_object.id}.index')

        if os.path.exists(
            self.website_storage_schemas_index_path
        ):
            self.website_storage_schemas_index = faiss.read_index(
                self.website_storage_schemas_index_path
            )

        else:
            self.website_storage_schemas_index = faiss.IndexIDMap(
                faiss.IndexFlatL2(
                    OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS
                )
            )

            faiss.write_index(
                self.website_storage_schemas_index,
                self.website_storage_schemas_index_path
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

    def search_within_website_item_chunks(
        self,
        website_url: str,
        query: str
    ):

        website_items = self.connection_object.storage_items.all()

        existing_urls = [
            item.website_url for item in website_items
        ]

        n_results = int(
            self.connection_object.search_instance_retrieval_limit
        )

        total_vectors = self.website_storage_schemas_index.ntotal

        k = min(
            WEBSITE_SEARCH_QUERY_SET_MAXIMUM_SIZE,
            total_vectors
        )

        query_vector = np.array(
            [
                self._generate_query_embedding(query)
            ],
            dtype=np.float32
        )

        if self.website_storage_schemas_index is None:
            raise ValueError("[search_within_website_item_chunks] FAISS index not initialized or loaded properly.")

        distances, ids = self.website_storage_schemas_index.search(
            query_vector,
            k=k
        )

        print(f"Unfiltered results have been found. Total: {len(ids[0])}")

        filtered_results = []

        # Post-filter the results by website URL

        if (
            website_url is not None and
            website_url != "" and
            website_url in existing_urls
        ):

            for item_id, distance in zip(
                ids[0],
                distances[0]
            ):

                if item_id == -1:
                    continue

                try:
                    instance = WebsiteItemChunkVectorData.objects.get(
                        id=item_id
                    )

                    # Filter by website URL

                    if instance.website_item.website_url == website_url:

                        filtered_results.append(
                            {
                                "id": instance.id,
                                "data": instance.raw_data,
                                "distance": distance,
                            }
                        )

                        if len(filtered_results) >= n_results:
                            break

                except WebsiteItemChunkVectorData.DoesNotExist:
                    logger.error(f"Website Item Chunk Instance with ID {item_id} not found in the database.")

            return filtered_results

        else:

            # Do not filter by website URL

            for item_id, distance in zip(ids[0], distances[0]):

                if item_id == -1:
                    continue

                try:

                    instance = WebsiteItemChunkVectorData.objects.get(
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

                except WebsiteItemChunkVectorData.DoesNotExist:
                    logger.error(f"Website Item Chunk Instance with ID {item_id} not found in the database.")

            return filtered_results
