#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: chunk_memory_tasks.py
#  Last Modified: 2024-09-26 22:02:31
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:44:49
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from langchain_text_splitters import RecursiveCharacterTextSplitter

from apps.datasource_knowledge_base.utils import MEMORY_DEFAULT_CHUNK_SIZE, MEMORY_DEFAULT_CHUNK_OVERLAP


def chunk_memory(message_text: str):
    chunks, error = [], None
    # Split the message into chunks
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=MEMORY_DEFAULT_CHUNK_SIZE,
        chunk_overlap=MEMORY_DEFAULT_CHUNK_OVERLAP
    )
    chunks = splitter.split_text(message_text)
    if chunks:
        print(f"[tasks.index_document_helper] Message chunked into {len(chunks)} chunk(s).")
    else:
        error = "[tasks.index_document_helper] Error chunking the message."
    return chunks, error
