#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: split_repository_into_chunks_tasks.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:46
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

from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)


def split_repository_into_chunks(connection_id, doc):
    from apps.datasource_codebase.models import CodeRepositoryStorageConnection

    conn = CodeRepositoryStorageConnection.objects.get(
        id=connection_id
    )

    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=conn.embedding_chunk_size,
        chunk_overlap=conn.embedding_chunk_overlap
    )

    logger.info(f"Splitting the repository into chunks: {doc['metadata']['document_id']}")

    chks = splitter.split_text(doc["page_content"])
    chks_cleaned = []

    for i, chk in enumerate(chks):
        doc["metadata"]["chunk_index"] = i

        clean_chunk = {
            "page_content": chk,
            "metadata": doc["metadata"]
        }

        chks_cleaned.append(clean_chunk)

    logger.info(f"Repository split into {len(chks_cleaned)} chunks.")
    return chks_cleaned
