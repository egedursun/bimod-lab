#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: chunk_memory_tasks.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:47
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

from apps.datasource_knowledge_base.utils import INTRA_MEMORY_INITIAL_CHUNK_SIZE, INTRA_MEMORY_INITIAL_CHUNK_OVERLAP


logger = logging.getLogger(__name__)


def chunk_memory(message_text: str):
    chks, error = [], None
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=INTRA_MEMORY_INITIAL_CHUNK_SIZE, chunk_overlap=INTRA_MEMORY_INITIAL_CHUNK_OVERLAP
    )
    chks = splitter.split_text(message_text)
    if chks:
        logger.info(f"[tasks.index_document_helper] Memory chunked successfully.")
        pass
    else:
        logger.error(f"[tasks.index_document_helper] Error chunking the message.")
        error = "[tasks.index_document_helper] Error chunking the message."
    return chks, error
