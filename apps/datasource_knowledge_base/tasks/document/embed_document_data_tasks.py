#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: embed_document_data_tasks.py
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
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging

from apps.core.vector_operations.vector_document.handler_methods.embedding_handler_document import (
    embed_document_helper
)


logger = logging.getLogger(__name__)


def embed_document_data(
    executor_params,
    document,
    path,
    number_of_chunks
):
    doc_id, doc_uuid = None, None

    try:
        doc_id, doc_uuid, error = embed_document_helper(
            executor_params=executor_params,
            document=document,
            path=path,
            number_of_chunks=number_of_chunks
        )

        logger.info(f"[tasks.embed_document_data] Document embedded successfully.")

    except Exception as e:
        logger.error(f"[tasks.embed_document_data] Error embedding the document: {e}")
        error = f"[tasks.embed_document_data] Error embedding the document: {e}"

    return doc_id, doc_uuid, error
