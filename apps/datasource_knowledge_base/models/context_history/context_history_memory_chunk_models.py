#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: context_history_memory_chunk_models.py
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.db import models


class ContextHistoryMemoryChunk(models.Model):
    """
    ContextHistoryMemoryChunk Model:
    - Purpose: Represents a chunk of a memory within a context history knowledge base, storing information about the chunk's content and its association with the memory and knowledge base.
    - Key Fields:
        - `context_history_base`: ForeignKey linking to the `ContextHistoryKnowledgeBaseConnection` model.
        - `memory`: ForeignKey linking to the `ContextHistoryMemory` model.
        - `chunk_number`: The sequence number of the chunk.
        - `chunk_content`: The text content of the chunk.
        - `knowledge_base_memory_uuid`, `chunk_uuid`: UUIDs for linking the chunk to the memory and knowledge base.
        - `created_at`, `updated_at`: Timestamps for creation and last update.
    """

    context_history_base = models.ForeignKey("ContextHistoryKnowledgeBaseConnection", on_delete=models.CASCADE)
    memory = models.ForeignKey("ContextHistoryMemory", on_delete=models.CASCADE, related_name='memory_chunks')

    chunk_number = models.IntegerField()
    chunk_content = models.TextField()  # This will be the text content of the chunk

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    knowledge_base_memory_uuid = models.CharField(max_length=1000, null=True, blank=True)
    chunk_uuid = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return (str(self.chunk_number) + " - " + self.memory.context_history_base.assistant.name + " - " +
                self.created_at.strftime("%Y%m%d%H%M%S"))

    class Meta:
        verbose_name = "Context History Memory Chunk"
        verbose_name_plural = "Context History Memory Chunks"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["context_history_base", "memory", "chunk_number"]),
            models.Index(fields=["context_history_base", "memory", "created_at"]),
            models.Index(fields=["context_history_base", "memory", "updated_at"]),
        ]
