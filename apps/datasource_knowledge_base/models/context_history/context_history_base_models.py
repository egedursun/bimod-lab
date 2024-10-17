#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: context_history_base_models.py
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
from apps.datasource_knowledge_base.utils import EMBEDDING_VECTORIZER_MODELS, build_weaviate_intra_memory_class_name


class ContextHistoryKnowledgeBaseConnection(models.Model):
    assistant = models.ForeignKey('assistants.Assistant', on_delete=models.CASCADE, default=1)
    chat = models.ForeignKey('multimodal_chat.MultimodalChat', on_delete=models.CASCADE, default=1)
    class_name = models.CharField(max_length=1000, null=True, blank=True)
    vectorizer = models.CharField(max_length=100, choices=EMBEDDING_VECTORIZER_MODELS, default="text2vec-openai")
    vectorizer_api_key = models.CharField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.assistant.name + " - " + self.created_at.strftime("%Y%m%d%H%M%S")

    class Meta:
        verbose_name = "Context History Knowledge Base Connection"
        verbose_name_plural = "Context History Knowledge Base Connections"
        ordering = ["-created_at"]
        unique_together = ['assistant', 'chat']
        indexes = [
            models.Index(fields=["assistant", "chat"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
            models.Index(fields=["class_name"]),
            models.Index(fields=["vectorizer"]),
        ]

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.vectorizer is None:
            self.vectorizer = "text2vec-openai"
        if self.class_name is None:
            self.class_name = build_weaviate_intra_memory_class_name()
        super().save(force_insert, force_update, using, update_fields)
        c = IntraContextMemoryExecutor(connection=self)
        if c is not None:
            o = c.create_chat_history_classes()
            if not o["status"]:
                pass

    def delete(self, using=None, keep_parents=False):
        c = IntraContextMemoryExecutor(connection=self)
        if c is not None:
            o = c.delete_chat_history_classes(class_name=self.class_name)
            if not o["status"]:
                pass
        super().delete(using, keep_parents)
