#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#


from apps.core.vector_operations.vector_document.vector_store_decoder import KnowledgeBaseSystemDecoder
from apps.datasource_knowledge_base.models import DocumentKnowledgeBaseConnection


def run_query_vector_store(c_id: int, vector_store_query: str, semantic_alpha: float):
    conn = DocumentKnowledgeBaseConnection.objects.get(id=c_id)
    try:
        client = KnowledgeBaseSystemDecoder().get(connection=conn)
        output = client.search_hybrid(query=vector_store_query, alpha=semantic_alpha)
    except Exception as e:
        error_msg = f"Error occurred while executing the knowledge base query: {str(e)}"
        return error_msg
    return output
