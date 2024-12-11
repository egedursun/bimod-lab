#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: embed_file_directory_schema_tasks.py
#  Last Modified: 2024-12-04 03:15:19
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-04 03:15:19
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

import faiss
import numpy as np

from apps.datasource_file_systems.utils import (
    OpenAIEmbeddingModels,
    OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS,
    VECTOR_INDEX_PATH_FILE_SYSTEM_DIRECTORY_SCHEMAS
)

logger = logging.getLogger(__name__)


def _generate_embedding(vector, raw_data):
    from apps.core.generative_ai.gpt_openai_manager import (
        OpenAIGPTClientManager
    )

    from apps.datasource_file_systems.models import (
        FileSystemDirectorySchemaChunkVectorData
    )

    vector: FileSystemDirectorySchemaChunkVectorData

    c = OpenAIGPTClientManager.get_naked_client(
        llm_model=vector.file_system.assistant.llm_model
    )

    raw_data_text = json.dumps(
        raw_data,
        indent=2
    )

    try:
        response = c.embeddings.create(
            input=raw_data_text,
            model=OpenAIEmbeddingModels.TEXT_EMBEDDING_3_LARGE
        )

        embedding_vector = response.data[0].embedding

        vector.vector_data = embedding_vector

    except Exception as e:
        logger.error(f"Error in generating embedding: {e}")

        vector.vector_data = []

    vector.raw_data = raw_data

    vector.save()


def _save_embedding(vector, index_path):
    if vector.vector_data:
        x = np.array(
            [
                vector.vector_data
            ],
            dtype=np.float32
        ).reshape(
            1,
            OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS
        )

        xids = np.array(
            [
                vector.id
            ],
            dtype=np.int64
        )

        if not os.path.exists(index_path):
            index = faiss.IndexIDMap(
                faiss.IndexFlatL2(
                    OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS
                )
            )

        else:
            index = faiss.read_index(
                index_path
            )

            if not isinstance(
                index,
                faiss.IndexIDMap
            ):
                index = faiss.IndexIDMap(index)

            index.remove_ids(
                xids
            )

        index.add_with_ids(
            x,
            xids
        )

        faiss.write_index(
            index,
            index_path
        )


def handle_embedding_task(
    vector_id: int,
    raw_data: dict
):
    from apps.datasource_file_systems.models import (
        FileSystemDirectorySchemaChunkVectorData
    )

    vector: FileSystemDirectorySchemaChunkVectorData = FileSystemDirectorySchemaChunkVectorData.objects.get(
        id=vector_id
    )

    storage_id = vector.file_system.id
    index_path = os.path.join(
        VECTOR_INDEX_PATH_FILE_SYSTEM_DIRECTORY_SCHEMAS,
        f'file_system_directory_schemas_index_{storage_id}.index'
    )

    if not vector:
        logger.error(f"Vector not found with ID: {vector}")

        return False

    _generate_embedding(
        vector=vector,
        raw_data=raw_data
    )

    _save_embedding(
        vector=vector,
        index_path=index_path
    )
