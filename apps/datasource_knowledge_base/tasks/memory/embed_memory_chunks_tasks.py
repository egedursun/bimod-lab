#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: embed_memory_chunks_tasks.py
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

from apps._services.knowledge_base.document.helpers.document_chunk_embedder import embed_memory_chunks_helper


def embed_memory_chunks(executor_params, chunks, memory_id, memory_uuid):
    try:
        error = embed_memory_chunks_helper(
            executor_params=executor_params,
            chunks=chunks,
            memory_id=memory_id,
            memory_uuid=memory_uuid
        )
    except Exception as e:
        error = f"[tasks.embed_memory_chunks] Error embedding the memory chunks: {e}"
    return error
