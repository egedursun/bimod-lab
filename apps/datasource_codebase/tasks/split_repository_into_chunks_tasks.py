#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_repository_into_chunks(connection_id, doc):
    from apps.datasource_codebase.models import CodeRepositoryStorageConnection
    connection = CodeRepositoryStorageConnection.objects.get(id=connection_id)
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=connection.embedding_chunk_size, chunk_overlap=connection.embedding_chunk_overlap
    )
    chunks = splitter.split_text(doc["page_content"])
    clean_chunks = []
    for i, chunk in enumerate(chunks):
        doc["metadata"]["chunk_index"] = i
        clean_chunk = {"page_content": chunk, "metadata": doc["metadata"]}
        clean_chunks.append(clean_chunk)
    print(f"[tasks.split_repository_into_chunks] Repository chunked into {len(clean_chunks)} chunk(s).")
    return clean_chunks
