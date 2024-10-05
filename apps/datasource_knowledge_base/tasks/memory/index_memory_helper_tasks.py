#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: index_memory_helper_tasks.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:45
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: index_memory_helper_tasks.py
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

from celery import shared_task


@shared_task
def index_memory_helper(connection_id, message_text):
    from apps.datasource_knowledge_base.models import ContextHistoryKnowledgeBaseConnection
    from apps._services.knowledge_base.memory.memory_executor import MemoryExecutor
    from apps.datasource_knowledge_base.tasks import chunk_memory

    output = {"status": True, "error": None}
    connection = ContextHistoryKnowledgeBaseConnection.objects.get(id=connection_id)
    executor = MemoryExecutor(connection=connection)
    try:
        print("[tasks.index_memory_helper] Indexing memory..")
        # Chunk the message
        chunks, error = chunk_memory(message_text=message_text)
        if error or not chunks:
            print(f"[tasks.index_memory_helper] Error chunking the chat history memory: {error}")
            output = {"status": False, "error": error}
            return output

        # Embed the memory doc
        number_of_chunks = len(chunks)
        doc_id, doc_uuid, error = executor.embed_memory(number_of_chunks=number_of_chunks)
        if error or not doc_id or not doc_uuid:
            print(f"[tasks.index_memory_helper] Error embedding the memory: {error}")
            output = {"status": False, "error": error}
            return output

        # Embed the memory chunks
        error = executor.embed_memory_chunks(chunks=chunks, memory_id=doc_id, memory_uuid=doc_uuid)
        if error:
            print(f"[tasks.index_memory_helper] Error embedding the memory chunks: {error}")
            output = {"status": False, "error": error}
            return output
        print("[tasks.index_memory_helper] Memory indexed successfully..")
    except Exception as e:
        output = {"status": False, "error": str(e)}
    return output
