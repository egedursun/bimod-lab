#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: embed_document_item_tasks.py
#  Last Modified: 2024-12-11 04:59:40
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-11 07:50:11
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
from typing import List

import faiss
import numpy as np

from apps.datasource_knowledge_base.models import (
    KnowledgeBaseDocument,
    DocumentChunkVectorData,
)

from apps.datasource_knowledge_base.utils import (
    VECTOR_INDEX_PATH_KNOWLEDGE_BASE_DOCUMENTS,
    OpenAIEmbeddingModels,
    OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS
)

from apps.datasource_knowledge_base.utils import (
    document_loader
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

logger = logging.getLogger(__name__)


def _generate_embedding(vector, raw_data):
    from apps.core.generative_ai.gpt_openai_manager import (
        OpenAIGPTClientManager
    )

    vector: DocumentChunkVectorData

    c = OpenAIGPTClientManager.get_naked_client(
        llm_model=vector.knowledge_base_document.knowledge_base.assistant.llm_model
    )

    raw_data_text = json.dumps(
        raw_data,
        indent=2
    )

    try:

        if vector.knowledge_base_document.knowledge_base.vectorizer == "text2vec-openai":

            response = c.embeddings.create(
                input=raw_data_text,
                model=OpenAIEmbeddingModels.TEXT_EMBEDDING_3_LARGE
            )

            embedding_vector = response.data[0].embedding
            vector.vector_data = embedding_vector

        else:
            logger.error(f"Invalid vectorizer type: {vector.knowledge_base_document.knowledge_base.vectorizer}")

            raise Exception("Invalid vectorizer type.")

    except Exception as e:
        logger.error(f"Error in generating embedding: {e}")
        vector.vector_data = []

    vector.raw_data = raw_data

    vector.save()


def _save_embedding(vector, index_path):
    if vector.vector_data:
        x = np.array(
            [vector.vector_data],
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
            index = faiss.read_index(index_path)

            if not isinstance(
                index,
                faiss.IndexIDMap
            ):
                index = faiss.IndexIDMap(index)

            index.remove_ids(xids)

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
    raw_data: dict,
):
    vector: DocumentChunkVectorData = DocumentChunkVectorData.objects.get(
        id=vector_id
    )

    storage_id = vector.knowledge_base_document.knowledge_base.id

    index_path = os.path.join(
        VECTOR_INDEX_PATH_KNOWLEDGE_BASE_DOCUMENTS,
        f'knowledge_base_storage_index_{storage_id}.index'
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


def load_and_index_document(
    items: List[KnowledgeBaseDocument]
) -> bool:

    if not items or len(items) == 0:
        print("No items to index, exiting the process.")
        logger.error("No items to index, exiting the process.")
        return False

    for item in items:
        item: KnowledgeBaseDocument

        try:

            extracted_document_content = document_loader(
                file_uri=item.document_uri,
                file_type=item.document_type
            )

            if not extracted_document_content:
                return False

            extracted_document_content_str = json.dumps(
                extracted_document_content,
                indent=2
            )

            splitter = RecursiveCharacterTextSplitter(
                extracted_document_content_str,
                chunk_size=item.knowledge_base.embedding_chunk_size,
                chunk_overlap=item.knowledge_base.embedding_chunk_overlap
            )

            chunks = splitter.split_text(extracted_document_content_str)

            item.n_chunks = int(len(chunks))
            item.save()

            try:
                for i, chunk in enumerate(chunks):

                    try:

                        chunk_vector_data = DocumentChunkVectorData.objects.create(
                            knowledge_base_document=item,
                            raw_data=chunk,
                        )

                        ##############################
                        # Save the Index to Vector DB
                        ##############################

                        handle_embedding_task(
                            vector_id=chunk_vector_data.id,
                            raw_data=chunk_vector_data.raw_data,
                        )

                        ##############################

                        item.n_chunks_indexed_status = int(
                            int(
                                item.n_chunks_indexed_status
                            ) + 1
                        )

                        item.save()

                        print("Chunk ", i + 1, " has been indexed & embedded successfully.")

                    except Exception as e:
                        logger.error(f"An error occurred while embedding chunk {i + 1}/{len(chunks)}: {e}")

                        continue

            except Exception as e:
                logger.error(f"An error occurred while embedding chunks: {e}")

                return False

            logger.info(f"Successfully updated the vector embeddings for Document with ID {item.id}.")
            logger.info("All chunks have been embedded successfully.")

        except Exception as e:
            logger.error(f"An error occurred while embedding document: {e}")

            continue

    return True
