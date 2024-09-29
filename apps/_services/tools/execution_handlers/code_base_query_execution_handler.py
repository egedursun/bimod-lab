#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: code_base_query_execution_handler.py
#  Last Modified: 2024-09-28 00:42:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:14:08
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from apps._services.codebase.codebase_decoder import CodeBaseDecoder
from apps.datasource_codebase.models import CodeRepositoryStorageConnection


def execute_code_base_query(connection_id: int, query: str, alpha: float):
    knowledge_base_connection = CodeRepositoryStorageConnection.objects.get(id=connection_id)
    print(f"[code_base_query_execution_handler.execute_code_base_query] Executing the code base query: {query}.")
    try:
        client = CodeBaseDecoder().get(connection=knowledge_base_connection)
        knowledge_base_response = client.search_hybrid(query=query, alpha=alpha)
    except Exception as e:
        error = (f"[code_base_query_execution_handler.execute_code_base_query] Error occurred while executing the "
                 f"code base query: {str(e)}")
        return error
    print(f"[code_base_query_execution_handler.execute_code_base_query] Code base query executed successfully.")
    return knowledge_base_response
