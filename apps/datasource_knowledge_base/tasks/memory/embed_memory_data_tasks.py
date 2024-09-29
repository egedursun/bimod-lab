#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: embed_memory_data_tasks.py
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

from apps._services.knowledge_base.document.helpers.document_embedder import embed_memory_helper


def embed_memory_data(executor_params, number_of_chunks):
    doc_id, doc_uuid = None, None
    try:
        doc_id, doc_uuid, error = embed_memory_helper(
            executor_params=executor_params,
            number_of_chunks=number_of_chunks
        )
    except Exception as e:
        error = f"[tasks.embed_memory_data] Error embedding the memory: {e}"
    return doc_id, doc_uuid, error
