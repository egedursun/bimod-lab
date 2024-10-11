#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: embed_document_chunks_tasks.py
#  Last Modified: 2024-10-05 01:39:47
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

from apps.core.vector_operations.vector_document.handler_methods.embedding_handler_chunk import (
    factory_embed_document_chunks_handler)


def embed_document_chunks(executor_params, chunks, path, document_id, document_uuid):
    try:
        error = factory_embed_document_chunks_handler(
            executor_params=executor_params, chunks=chunks, path=path, document_id=document_id,
            document_uuid=document_uuid
        )
    except Exception as e:
        error = f"[tasks.embed_document_chunks] Error embedding the document chunks: {e}"
    return error
