#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: embed_memory_data_tasks.py
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

from apps.core.vector_operations.vector_document.handler_methods.embedding_handler_document import embed_memory_helper


def embed_memory_data(executor_params, number_of_chunks):
    doc_id, doc_uuid = None, None
    try:
        doc_id, doc_uuid, error = embed_memory_helper(
            executor_params=executor_params, number_of_chunks=number_of_chunks
        )
    except Exception as e:
        error = f"[tasks.embed_memory_data] Error embedding the memory: {e}"
    return doc_id, doc_uuid, error
