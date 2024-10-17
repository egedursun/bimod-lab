#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: context_history_memory_models.py
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
#   For permission inquiries, please contact: admin@Bimod.io.
#
#
#
#

from django.db import models

from apps.core.vector_operations.intra_context_memory.memory_executor import IntraContextMemoryExecutor


class ContextHistoryMemory(models.Model):
    context_history_base = models.ForeignKey("ContextHistoryKnowledgeBaseConnection", on_delete=models.CASCADE,
                                             related_name='context_history_memories')
    memory_name = models.CharField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
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
        c = IntraContextMemoryExecutor(connection=self.context_history_base)
        if c is not None:
            o = c.delete_chat_history_document(
                class_name=self.context_history_base.class_name,
                document_uuid=self.knowledge_base_memory_uuid)
            if not o["status"]:
                pass
        super().delete(using, keep_parents)
