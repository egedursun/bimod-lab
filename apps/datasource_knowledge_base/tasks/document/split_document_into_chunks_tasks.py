#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: split_document_into_chunks_tasks.py
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_document_into_chunks(connection_id, doc):
    from apps.datasource_knowledge_base.models import DocumentKnowledgeBaseConnection
    conn = DocumentKnowledgeBaseConnection.objects.get(id=connection_id)
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=conn.embedding_chunk_size, chunk_overlap=conn.embedding_chunk_overlap
    )
    chks = splitter.split_text(doc["page_content"])
    chks_cleaned = []
    for i, chk in enumerate(chks):
        doc["metadata"]["chunk_index"] = i
        chk_clean = {"page_content": chk, "metadata": doc["metadata"]}
        chks_cleaned.append(chk_clean)
    return chks_cleaned
