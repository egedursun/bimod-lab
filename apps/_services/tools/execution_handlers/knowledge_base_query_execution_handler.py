#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: knowledge_base_query_execution_handler.py
#  Last Modified: 2024-09-28 00:42:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:14:32
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from apps._services.knowledge_base.document.knowledge_base_decoder import KnowledgeBaseSystemDecoder
from apps.datasource_knowledge_base.models import DocumentKnowledgeBaseConnection


def execute_knowledge_base_query(connection_id: int, query: str, alpha: float):
    knowledge_base_connection = DocumentKnowledgeBaseConnection.objects.get(id=connection_id)
    print(
        f"[knowledge_base_query_execution_handler.execute_knowledge_base_query] Executing the knowledge base query: {query}.")
    try:
        client = KnowledgeBaseSystemDecoder().get(connection=knowledge_base_connection)
        knowledge_base_response = client.search_hybrid(query=query, alpha=alpha)
    except Exception as e:
        error = (f"[knowledge_base_query_execution_handler.execute_knowledge_base_query] Error occurred while "
                 f"executing the knowledge base query: {str(e)}")
        return error
    print(f"[knowledge_base_query_execution_handler.execute_knowledge_base_query] Knowledge base query executed "
          f"successfully.")
    return knowledge_base_response
