#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: embed_repository_data_tasks.py
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

from apps.core.codebase.handler_methods.embedding_handler_repo import (
    embed_repository_helper
)

logger = logging.getLogger(__name__)


def embed_repository_data(
    executor_params,
    document,
    path,
    number_of_chunks
):

    doc_id, doc_uuid = None, None

    try:
        doc_id, doc_uuid, error = embed_repository_helper(
            executor_params=executor_params,
            document=document,
            path=path,
            number_of_chunks=number_of_chunks
        )

    except Exception as e:
        logger.error(f"[tasks.embed_repository_data] Error embedding the repository: {e}")
        error = f"[tasks.embed_repository_data] Error embedding the repository: {e}"

    logger.info(f"[tasks.embed_repository_data] Repository embedded successfully.")
    return doc_id, doc_uuid, error
