#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: embed_repository_item_tasks.py
#  Last Modified: 2024-12-11 08:01:19
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-11 09:02:29
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
from uuid import uuid4

import faiss
import numpy as np

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from apps.datasource_codebase.models import (
    CodeBaseRepository,
    CodeBaseRepositoryChunk,
)

from apps.datasource_codebase.utils import (
    VECTOR_INDEX_PATH_CODEBASE_REPOSITORIES,
    OpenAIEmbeddingModels,
    OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS
)

logger = logging.getLogger(__name__)


def load_and_index_repository(
    item_id: int
) -> bool:
    item: CodeBaseRepository = CodeBaseRepository.objects.get(
        id=item_id
    )

    if not item:
        return False

    complete_content, cloned_repository_path = _load_repository(
        item,
    )

    complete_content_string = json.dumps(
        complete_content,
        indent=2
    )

    splitter = RecursiveCharacterTextSplitter(
        complete_content_string,
        chunk_size=item.knowledge_base.embedding_chunk_size,
        chunk_overlap=item.knowledge_base.embedding_chunk_overlap
    )

    chunks = splitter.split_text(complete_content_string)

    item.n_chunks = int(len(chunks))
    item.save()

    try:
        for i, chunk in enumerate(chunks):

            try:

                chunk_vector_data = CodeBaseRepositoryChunk.objects.create(
                    repository_item=item,
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

            except Exception as e:
                logger.error(f"An error occurred while embedding chunk {i + 1}/{len(chunks)}: {e}")

                continue

    except Exception as e:
        logger.error(f"An error occurred while embedding chunks: {e}")

        return False

    logger.info(f"Successfully updated the vector embeddings for Code Repository with ID {item.id}.")
    logger.info("All chunks have been embedded successfully.")

    try:
        # Clean the cloned repository
        os.remove(cloned_repository_path)
    except Exception as e:
        logger.error(f"An error occurred while cleaning the cloned repository: {e}")

    return True


def _load_repository(
    item: CodeBaseRepository
) -> dict:
    item: CodeBaseRepository

    repository_content, cloned_repository_path = repository_loader(
        item=item
    )

    return repository_content, cloned_repository_path


def handle_embedding_task(
    vector_id: int,
    raw_data: dict,
):
    vector: CodeBaseRepositoryChunk = CodeBaseRepositoryChunk.objects.get(
        id=vector_id
    )

    storage_id = vector.repository_item.knowledge_base.id

    index_path = os.path.join(
        VECTOR_INDEX_PATH_CODEBASE_REPOSITORIES,
        f'codebase_storage_index_{storage_id}.index'
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


def repository_loader(
    item: CodeBaseRepository
) -> dict | None:
    result = {
        "page_content": "",
        "metadata": {}
    }

    formatted_content = ""

    repository_uri = item.repository_uri

    cloned_repository_path = _clone_repository(
        repository_uri=repository_uri
    )

    if not cloned_repository_path:
        logger.error(f"[WeaviateExecutor.repository_loader] Error cloning repository: {repository_uri}")

        return None

    try:
        for root, dirs, files in os.walk(cloned_repository_path):
            for file in files:
                file_path = os.path.join(root, file)

                if not is_supported_file(file_path):
                    logger.info(f"[WeaviateExecutor.repository_loader] Skipping unsupported file: {file_path}")
                    continue

                content_lines = extract_file_content_and_metadata(file_path)

                if not content_lines:
                    logger.error(
                        f"[WeaviateExecutor.repository_loader] Error extracting file content: {file_path}")
                    continue

                formatted_content += assign_line_numbers_and_filename_to_line(
                    str(file_path),
                    content_lines
                )

                formatted_content += "\n"

                logger.info(f"[WeaviateExecutor.repository_loader] Loaded file: {file_path}")

    except Exception as e:
        logger.error(f"[WeaviateExecutor.repository_loader] Error loading repository: {cloned_repository_path}")

        return None

    result["page_content"] = formatted_content
    logger.info(f"[WeaviateExecutor.repository_loader] Loaded repository: {cloned_repository_path}")

    return result, cloned_repository_path


def _clone_repository(
    repository_uri: str
) -> str:
    uuid_str = str(uuid4())
    assigned_path = f"/tmp/{uuid_str}"

    try:
        os.system(f"git clone {repository_uri} {assigned_path}")
        print(f"Cloned repository: {repository_uri}")
        logger.info(f"Cloned repository: {repository_uri}")

    except Exception as e:
        print(f"Error cloning repository: {repository_uri}")
        logger.error(f"Error cloning repository: {repository_uri}")

        return None

    return assigned_path


def is_supported_file(
    file_path: str
) -> bool:
    from apps.datasource_codebase.utils import (
        SupportedCodeFileTypes
    )

    supported_files = SupportedCodeFileTypes.as_list()
    file_extension = "." + file_path.split(".")[-1]

    if file_extension in supported_files:
        logger.info(f"Supported file: {file_path}")
        return True

    logger.info(f"Unsupported file: {file_path}")

    return False


def extract_file_content_and_metadata(file_path: str) -> list[str] | None:
    content = []

    try:
        with open(file_path, "r") as f:
            content = f.readlines()

    except Exception as e:
        logger.error(
            f"Error extracting file content: {file_path}")
        pass

    return content


def assign_line_numbers_and_filename_to_line(
    file_path: str,
    content: list
) -> str:
    accumulated_content = ""

    try:
        for i, line in enumerate(content):
            accumulated_content += f"[File Path: {file_path}] | [Line Number: {i}] --- {line}"

    except Exception as e:
        logger.error(f"Error assigning line numbers and filename to line: {file_path}")

        return accumulated_content

    logger.info(f"Assigned line numbers and filename to line: {file_path}")

    return accumulated_content


def _generate_embedding(vector, raw_data):
    from apps.core.generative_ai.gpt_openai_manager import (
        OpenAIGPTClientManager
    )

    vector: CodeBaseRepositoryChunk

    c = OpenAIGPTClientManager.get_naked_client(
        llm_model=vector.repository_item.knowledge_base.assistant.llm_model
    )

    raw_data_text = json.dumps(
        raw_data,
        indent=2
    )

    try:

        if vector.repository_item.knowledge_base.vectorizer == "text2vec-openai":

            response = c.embeddings.create(
                input=raw_data_text,
                model=OpenAIEmbeddingModels.TEXT_EMBEDDING_3_LARGE
            )

            embedding_vector = response.data[0].embedding
            vector.vector_data = embedding_vector

        else:
            logger.error(f"Invalid vectorizer type: {vector.repository_item.knowledge_base.vectorizer}")

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
