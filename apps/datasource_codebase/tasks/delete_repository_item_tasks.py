#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_repository_item_tasks.py
#  Last Modified: 2024-12-11 08:01:19
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-11 08:59:57
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

import faiss
import numpy as np

from apps.datasource_codebase.models import (
    CodeBaseRepository,
    CodeRepositoryStorageConnection,
    VECTOR_INDEX_PATH_CODEBASE_REPOSITORIES,
    CodeBaseRepositoryChunk
)

logger = logging.getLogger(__name__)


def handle_delete_repository_item(item: CodeBaseRepository):
    try:
        success = _clean_previous_data(
            item=item
        )

        if success is False:
            logger.error(f"An error occurred while deleting the data for Code Repository item with ID: {item.id}")

            return False

        item.delete()

        logger.info(f"Successfully deleted the data for Code Repository item with ID: {item.id}")
        return True

    except Exception as e:
        logger.error(f"An error occurred while deleting the data for Code Repository item with ID: {item.id}")

        return False


def _clean_previous_data(item: CodeBaseRepository) -> bool:
    try:

        item.n_chunks_indexed_status = 0
        item.n_chunks = 0
        item.save()

        storage = item.knowledge_base
        storage: CodeRepositoryStorageConnection
        storage_id = storage.id

        index_path = os.path.join(
            VECTOR_INDEX_PATH_CODEBASE_REPOSITORIES,
            f'codebase_storage_index_{storage_id}.index'
        )

        previous_vectors = CodeBaseRepositoryChunk.objects.filter(
            repository_item=item
        )

        if not previous_vectors.exists():
            logger.info(f"No previous vector data found for Document item with ID: {item.id}, skipping...")

        else:
            vector_ids = list(
                previous_vectors.values_list(
                    'id',
                    flat=True
                )
            )

            previous_vectors.delete()

            logger.info(f"Deleted {len(vector_ids)} previous vector ORM objects for Document item with ID: {item.id}")

            if os.path.exists(index_path):

                index = faiss.read_index(index_path)

                if not isinstance(
                    index,
                    faiss.IndexIDMap
                ):
                    index = faiss.IndexIDMap(index)

                xids = np.array(
                    vector_ids,
                    dtype=np.int64
                )

                index.remove_ids(xids)

                faiss.write_index(
                    index,
                    index_path
                )

                logger.info(
                    f"Removed vectors with IDs {vector_ids} from FAISS index for Code Repository item {item.id}.")

            else:
                logger.info(f"FAISS index file not found at {index_path}, nothing to clean...")

        logger.info(f"Successfully cleaned the previous data for Code Repository item with ID: {item.id}.")

        return True

    except Exception as e:

        logger.error(
            f"An error occurred while cleaning the previous data for Code Repository item with ID: {item.id}: {e}")

        return False
