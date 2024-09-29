#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: memory_query_execution_handler.py
#  Last Modified: 2024-09-28 00:42:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:14:35
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from apps._services.knowledge_base.memory.memory_executor import MemoryExecutor
from apps.datasource_knowledge_base.models import ContextHistoryKnowledgeBaseConnection


def execute_memory_query(connection_id: int, query: str, alpha: float):
    memory_connection = ContextHistoryKnowledgeBaseConnection.objects.get(id=connection_id)
    print(f"[memory_query_execution_handler.execute_memory_query] Executing the memory query: {query}.")
    try:
        c = MemoryExecutor(connection=memory_connection)
        memory_response = c.search_hybrid(query=query, alpha=alpha)
    except Exception as e:
        error = (f"[memory_query_execution_handler.execute_memory_query] Error occurred while executing the memory "
                 f"query: {str(e)}")
        return error
    print(f"[memory_query_execution_handler.execute_memory_query] Memory query executed successfully.")
    return memory_response
