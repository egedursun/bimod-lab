#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: core_service_vector_store_query.py
#  Last Modified: 2024-10-05 02:31:01
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:35
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
import traceback

from apps.core.vector_operations.vector_store_executor import (
    VectorStoreExecutor
)

from apps.datasource_knowledge_base.models import (
    DocumentKnowledgeBaseConnection
)

logger = logging.getLogger(__name__)


def run_query_search_document_data(
    connection_id: str,
    document_file_name: str,
    query: str
):
    try:
        connection = DocumentKnowledgeBaseConnection.objects.get(
            id=connection_id
        )

        if not connection:
            return f"Connection with ID: {connection_id} does not exist."

        xc = VectorStoreExecutor(
            connection_id=connection_id
        )

        output = xc.search_within_document_chunks(
            document_file_name=document_file_name,
            query=query
        )

    except Exception as e:
        logger.error(f"Error occurred while executing the Document Data Search query: {str(e)}")
        logger.error(traceback.format_exc())
        error_msg = f"Error occurred while executing the Document Data Search query: {str(e)}"

        return error_msg

    return output
