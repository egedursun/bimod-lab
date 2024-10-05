#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: context_history_memory_models.py
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
#  File: context_history_memory_models.py
#  Last Modified: 2024-09-26 22:02:31
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:42:30
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.db import models

from apps._services.knowledge_base.memory.memory_executor import MemoryExecutor


class ContextHistoryMemory(models.Model):
    """
    ContextHistoryMemory Model:
    - Purpose: Represents a memory within a context history knowledge base, storing information about the memory's association with the knowledge base and related chunks.
    - Key Fields:
        - `context_history_base`: ForeignKey linking to the `ContextHistoryKnowledgeBaseConnection` model.
        - `memory_name`: Metadata field for the memory name.
        - `knowledge_base_memory_uuid`: UUID for linking the memory to the knowledge base system.
        - `memory_chunks`: ManyToManyField linking to the memory chunks.
        - `created_at`, `updated_at`: Timestamps for creation and last update.
    - Methods:
        - `delete()`: Overridden to remove the memory from the knowledge base system.
    """

    context_history_base = models.ForeignKey("ContextHistoryKnowledgeBaseConnection", on_delete=models.CASCADE,
                                             related_name='context_history_memories')
    memory_name = models.CharField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # to associate the element with the Weaviate object
    knowledge_base_memory_uuid = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.context_history_base.assistant.name + " - " + self.created_at.strftime("%Y%m%d%H%M%S")

    class Meta:
        verbose_name = "Context History Memory"
        verbose_name_plural = "Context History Memories"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["context_history_base", "memory_name"]),
            models.Index(fields=["context_history_base", "created_at"]),
            models.Index(fields=["context_history_base", "updated_at"]),
        ]

    def delete(self, using=None, keep_parents=False):
        # delete the document from Weaviate
        client = MemoryExecutor(connection=self.context_history_base)
        if client is not None:
            result = client.delete_chat_history_document(
                class_name=self.context_history_base.class_name,
                document_uuid=self.knowledge_base_memory_uuid)
            if not result["status"]:
                print(f"[ContextHistoryMemory.delete] Error deleting Weaviate document: {result['error']}")
        # delete the object from ORM
        super().delete(using, keep_parents)
