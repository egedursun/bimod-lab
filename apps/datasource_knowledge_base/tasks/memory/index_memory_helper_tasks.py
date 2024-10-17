#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: index_memory_helper_tasks.py
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
from celery import shared_task


@shared_task
def index_memory_helper(connection_id, message_text):
    from apps.datasource_knowledge_base.models import ContextHistoryKnowledgeBaseConnection
    from apps.core.vector_operations.intra_context_memory.memory_executor import IntraContextMemoryExecutor
    from apps.datasource_knowledge_base.tasks import chunk_memory

    output = {
        "status": True,
        "error": None
    }
    conn = ContextHistoryKnowledgeBaseConnection.objects.get(id=connection_id)
    xc = IntraContextMemoryExecutor(connection=conn)
    try:
        chks, error = chunk_memory(message_text=message_text)
        if error or not chks:
            output = {
                "status": False,
                "error": error
            }
            return output

        n_chks = len(chks)
        doc_id, doc_uuid, error = xc.embed_memory(number_of_chunks=n_chks)
        if error or not doc_id or not doc_uuid:
            output = {
                "status": False,
                "error": error
            }
            return output

        error = xc.embed_memory_chunks(chunks=chks, memory_id=doc_id, memory_uuid=doc_uuid)
        if error:
            output = {
                "status": False,
                "error": error
            }
            return output
    except Exception as e:
        output = {
            "status": False,
            "error": str(e)
        }
    return output
