#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: multimodal_chat_models.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:43
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

#
from django.db import models

from apps._services.knowledge_base.memory.memory_executor import MemoryExecutor
from apps.assistants.utils import ContextOverflowStrategyNames
from apps.datasource_knowledge_base.models import ContextHistoryKnowledgeBaseConnection
from apps.multimodal_chat.utils import CHAT_SOURCES


class MultimodalChat(models.Model):
    """
    MultimodalChat Model:
    - Purpose: Represents a multimodal chat session involving an assistant and a user. It stores chat messages, transactions, context memory connections, and starred messages. It also includes metadata such as the chat source and whether the chat is archived.
    - Key Fields:
        - `organization`: ForeignKey linking to the `Organization` model.
        - `assistant`: ForeignKey linking to the `Assistant` model.
        - `user`: ForeignKey linking to the `User` model.
        - `chat_name`: The name of the chat session.
        - `created_by_user`: ForeignKey linking to the `User` who created the chat.
        - `chat_messages`: ManyToManyField linking to `MultimodalChatMessage` models representing the chat's messages.
        - `transactions`: ManyToManyField linking to `LLMTransaction` models associated with the chat.
        - `context_memory_connection`: OneToOneField linking to a `ContextHistoryKnowledgeBaseConnection` for managing chat context.
        - `starred_messages`: ManyToManyField linking to `StarredMessage` models representing starred messages in the chat.
        - `is_archived`: Boolean field indicating whether the chat is archived.
        - `chat_source`: Field specifying the source of the chat (e.g., app, API).
        - `created_at`, `updated_at`: Timestamps for creation and last update.
    - Methods:
        - `save()`: Overridden to handle context memory connection creation and related logic.
        - `delete()`: Overridden to manage the deletion of context memory connections.
    - Meta:
        - `verbose_name`: "Multimodal Chat"
        - `verbose_name_plural`: "Multimodal Chats"
        - `ordering`: Orders chats by creation date in descending order.
        - `indexes`: Indexes on various fields for optimized queries.
    """

    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE)
    assistant = models.ForeignKey('assistants.Assistant', on_delete=models.CASCADE,
                                  related_name='multimodal_chats', null=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='multimodal_chats', null=True)
    chat_name = models.CharField(max_length=255)
    created_by_user = models.ForeignKey('auth.User', on_delete=models.CASCADE,
                                        related_name='multimodal_chats_created_by_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Context Memory
    context_memory_connection = models.OneToOneField(ContextHistoryKnowledgeBaseConnection, on_delete=models.CASCADE,
                                                     related_name='multimodal_chat', null=True, blank=True)
    transactions = models.ManyToManyField('llm_transaction.LLMTransaction', related_name='multimodal_chats',
                                          blank=True)

    # For archiving the chats
    is_archived = models.BooleanField(default=False)
    # Management for APIs
    chat_source = models.CharField(max_length=100, choices=CHAT_SOURCES, default="app")

    def __str__(self):
        return self.chat_name + " - " + self.assistant.name + " - " + self.user.username

    class Meta:
        verbose_name = "Multimodal Chat"
        verbose_name_plural = "Multimodal Chats"
        ordering = ["-created_at"]
        indexes = [
            # Single-field indexes
            models.Index(fields=['id']),
            models.Index(fields=['organization']),
            models.Index(fields=['assistant']),
            models.Index(fields=['user']),
            models.Index(fields=['chat_source']),
            models.Index(fields=['is_archived']),
            models.Index(fields=['created_by_user']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),

            # Two-field composite indexes
            models.Index(fields=['id', 'organization']),
            models.Index(fields=['id', 'assistant']),
            models.Index(fields=['id', 'user']),
            models.Index(fields=['id', 'chat_source']),
            models.Index(fields=['id', 'is_archived']),
            models.Index(fields=['id', 'created_by_user']),
            models.Index(fields=['id', 'created_at']),
            models.Index(fields=['id', 'updated_at']),
            models.Index(fields=['organization', 'assistant']),
            models.Index(fields=['organization', 'user']),
            models.Index(fields=['organization', 'chat_source']),
            models.Index(fields=['organization', 'is_archived']),
            models.Index(fields=['organization', 'created_by_user']),
            models.Index(fields=['organization', 'created_at']),
            models.Index(fields=['organization', 'updated_at']),
            models.Index(fields=['assistant', 'user']),
            models.Index(fields=['assistant', 'chat_source']),
            models.Index(fields=['assistant', 'is_archived']),
            models.Index(fields=['assistant', 'created_by_user']),
            models.Index(fields=['assistant', 'created_at']),
            models.Index(fields=['assistant', 'updated_at']),
            models.Index(fields=['user', 'chat_source']),
            models.Index(fields=['user', 'is_archived']),
            models.Index(fields=['user', 'created_by_user']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['user', 'updated_at']),
            models.Index(fields=['chat_source', 'is_archived']),
            models.Index(fields=['chat_source', 'created_by_user']),
            models.Index(fields=['chat_source', 'created_at']),
            models.Index(fields=['chat_source', 'updated_at']),
            models.Index(fields=['is_archived', 'created_by_user']),
            models.Index(fields=['is_archived', 'created_at']),
            models.Index(fields=['is_archived', 'updated_at']),
            models.Index(fields=['created_by_user', 'created_at']),
            models.Index(fields=['created_by_user', 'updated_at']),
            models.Index(fields=['created_at', 'updated_at']),

            # Three-field composite indexes
            models.Index(fields=['id', 'organization', 'assistant']),
            models.Index(fields=['id', 'organization', 'user']),
            models.Index(fields=['id', 'organization', 'chat_source']),
            models.Index(fields=['id', 'organization', 'is_archived']),
            models.Index(fields=['id', 'organization', 'created_by_user']),
            models.Index(fields=['id', 'organization', 'created_at']),
            models.Index(fields=['id', 'organization', 'updated_at']),
            models.Index(fields=['id', 'assistant', 'user']),
            models.Index(fields=['id', 'assistant', 'chat_source']),
            models.Index(fields=['id', 'assistant', 'is_archived']),
            models.Index(fields=['id', 'assistant', 'created_by_user']),
            models.Index(fields=['id', 'assistant', 'created_at']),
            models.Index(fields=['id', 'assistant', 'updated_at']),
            models.Index(fields=['id', 'user', 'chat_source']),
            models.Index(fields=['id', 'user', 'is_archived']),
            models.Index(fields=['id', 'user', 'created_by_user']),
            models.Index(fields=['id', 'user', 'created_at']),
            models.Index(fields=['id', 'user', 'updated_at']),
            models.Index(fields=['id', 'chat_source', 'is_archived']),
            models.Index(fields=['id', 'chat_source', 'created_by_user']),
            models.Index(fields=['id', 'chat_source', 'created_at']),
            models.Index(fields=['id', 'chat_source', 'updated_at']),
            models.Index(fields=['id', 'is_archived', 'created_by_user']),
            models.Index(fields=['id', 'is_archived', 'created_at']),
            models.Index(fields=['id', 'is_archived', 'updated_at']),
            models.Index(fields=['id', 'created_by_user', 'created_at']),
            models.Index(fields=['id', 'created_by_user', 'updated_at']),
            models.Index(fields=['id', 'created_at', 'updated_at']),
            models.Index(fields=['organization', 'assistant', 'user']),
            models.Index(fields=['organization', 'assistant', 'chat_source']),
            models.Index(fields=['organization', 'assistant', 'is_archived']),
            models.Index(fields=['organization', 'assistant', 'created_by_user']),
            models.Index(fields=['organization', 'assistant', 'created_at']),
            models.Index(fields=['organization', 'assistant', 'updated_at']),
            models.Index(fields=['organization', 'user', 'chat_source']),
            models.Index(fields=['organization', 'user', 'is_archived']),
            models.Index(fields=['organization', 'user', 'created_by_user']),
            models.Index(fields=['organization', 'user', 'created_at']),
            models.Index(fields=['organization', 'user', 'updated_at']),
            models.Index(fields=['organization', 'chat_source', 'is_archived']),
            models.Index(fields=['organization', 'chat_source', 'created_by_user']),
            models.Index(fields=['organization', 'chat_source', 'created_at']),
            models.Index(fields=['organization', 'chat_source', 'updated_at']),
            models.Index(fields=['organization', 'is_archived', 'created_by_user']),
            models.Index(fields=['organization', 'is_archived', 'created_at']),
            models.Index(fields=['organization', 'is_archived', 'updated_at']),
            models.Index(fields=['organization', 'created_by_user', 'created_at']),
            models.Index(fields=['organization', 'created_by_user', 'updated_at']),
            models.Index(fields=['organization', 'created_at', 'updated_at']),
            models.Index(fields=['assistant', 'user', 'chat_source']),
            models.Index(fields=['assistant', 'user', 'is_archived']),
            models.Index(fields=['assistant', 'user', 'created_by_user']),
            models.Index(fields=['assistant', 'user', 'created_at']),
            models.Index(fields=['assistant', 'user', 'updated_at']),
            models.Index(fields=['assistant', 'chat_source', 'is_archived']),
            models.Index(fields=['assistant', 'chat_source', 'created_by_user']),
            models.Index(fields=['assistant', 'chat_source', 'created_at']),
            models.Index(fields=['assistant', 'chat_source', 'updated_at']),
            models.Index(fields=['assistant', 'is_archived', 'created_by_user']),
            models.Index(fields=['assistant', 'is_archived', 'created_at']),
            models.Index(fields=['assistant', 'is_archived', 'updated_at']),
            models.Index(fields=['assistant', 'created_by_user', 'created_at']),
            models.Index(fields=['assistant', 'created_by_user', 'updated_at']),
            models.Index(fields=['assistant', 'created_at', 'updated_at']),
            models.Index(fields=['user', 'chat_source', 'is_archived']),
            models.Index(fields=['user', 'chat_source', 'created_by_user']),
            models.Index(fields=['user', 'chat_source', 'created_at']),
            models.Index(fields=['user', 'chat_source', 'updated_at']),
            models.Index(fields=['user', 'is_archived', 'created_by_user']),
            models.Index(fields=['user', 'is_archived', 'created_at']),
            models.Index(fields=['user', 'is_archived', 'updated_at']),
            models.Index(fields=['user', 'created_by_user', 'created_at']),
            models.Index(fields=['user', 'created_by_user', 'updated_at']),
            models.Index(fields=['user', 'created_at', 'updated_at']),
            models.Index(fields=['chat_source', 'is_archived', 'created_by_user']),
            models.Index(fields=['chat_source', 'is_archived', 'created_at']),
            models.Index(fields=['chat_source', 'is_archived', 'updated_at']),
            models.Index(fields=['chat_source', 'created_by_user', 'created_at']),
            models.Index(fields=['chat_source', 'created_by_user', 'updated_at']),
            models.Index(fields=['chat_source', 'created_at', 'updated_at']),
            models.Index(fields=['is_archived', 'created_by_user', 'created_at']),
            models.Index(fields=['is_archived', 'created_by_user', 'updated_at']),
            models.Index(fields=['is_archived', 'created_at', 'updated_at']),
            models.Index(fields=['created_by_user', 'created_at', 'updated_at']),

            # Four-field composite indexes
            models.Index(fields=['id', 'organization', 'assistant', 'user']),
            models.Index(fields=['id', 'organization', 'assistant', 'chat_source']),
            models.Index(fields=['id', 'organization', 'assistant', 'is_archived']),
            models.Index(fields=['id', 'organization', 'assistant', 'created_by_user']),
            models.Index(fields=['id', 'organization', 'assistant', 'created_at']),
            models.Index(fields=['id', 'organization', 'assistant', 'updated_at']),
            models.Index(fields=['id', 'organization', 'user', 'chat_source']),
            models.Index(fields=['id', 'organization', 'user', 'is_archived']),
            models.Index(fields=['id', 'organization', 'user', 'created_by_user']),
            models.Index(fields=['id', 'organization', 'user', 'created_at']),
            models.Index(fields=['id', 'organization', 'user', 'updated_at']),
            models.Index(fields=['id', 'organization', 'chat_source', 'is_archived']),
            models.Index(fields=['id', 'organization', 'chat_source', 'created_by_user']),
            models.Index(fields=['id', 'organization', 'chat_source', 'created_at']),
            models.Index(fields=['id', 'organization', 'chat_source', 'updated_at']),
            models.Index(fields=['id', 'organization', 'is_archived', 'created_by_user']),
            models.Index(fields=['id', 'organization', 'is_archived', 'created_at']),
            models.Index(fields=['id', 'organization', 'is_archived', 'updated_at']),
            models.Index(fields=['id', 'organization', 'created_by_user', 'created_at']),
            models.Index(fields=['id', 'organization', 'created_by_user', 'updated_at']),
            models.Index(fields=['id', 'organization', 'created_at', 'updated_at']),
            models.Index(fields=['id', 'assistant', 'user', 'chat_source']),
            models.Index(fields=['id', 'assistant', 'user', 'is_archived']),
            models.Index(fields=['id', 'assistant', 'user', 'created_by_user']),
            models.Index(fields=['id', 'assistant', 'user', 'created_at']),
            models.Index(fields=['id', 'assistant', 'user', 'updated_at']),
            models.Index(fields=['id', 'assistant', 'chat_source', 'is_archived']),
            models.Index(fields=['id', 'assistant', 'chat_source', 'created_by_user']),
            models.Index(fields=['id', 'assistant', 'chat_source', 'created_at']),
            models.Index(fields=['id', 'assistant', 'chat_source', 'updated_at']),
            models.Index(fields=['id', 'assistant', 'is_archived', 'created_by_user']),
            models.Index(fields=['id', 'assistant', 'is_archived', 'created_at']),
            models.Index(fields=['id', 'assistant', 'is_archived', 'updated_at']),
            models.Index(fields=['id', 'assistant', 'created_by_user', 'created_at']),
            models.Index(fields=['id', 'assistant', 'created_by_user', 'updated_at']),
            models.Index(fields=['id', 'assistant', 'created_at', 'updated_at']),
            models.Index(fields=['id', 'user', 'chat_source', 'is_archived']),
            models.Index(fields=['id', 'user', 'chat_source', 'created_by_user']),
            models.Index(fields=['id', 'user', 'chat_source', 'created_at']),
            models.Index(fields=['id', 'user', 'chat_source', 'updated_at']),
            models.Index(fields=['id', 'user', 'is_archived', 'created_by_user']),
            models.Index(fields=['id', 'user', 'is_archived', 'created_at']),
            models.Index(fields=['id', 'user', 'is_archived', 'updated_at']),
            models.Index(fields=['id', 'user', 'created_by_user', 'created_at']),
            models.Index(fields=['id', 'user', 'created_by_user', 'updated_at']),
            models.Index(fields=['id', 'user', 'created_at', 'updated_at']),
            models.Index(fields=['id', 'chat_source', 'is_archived', 'created_by_user']),
            models.Index(fields=['id', 'chat_source', 'is_archived', 'created_at']),
            models.Index(fields=['id', 'chat_source', 'is_archived', 'updated_at']),
            models.Index(fields=['id', 'chat_source', 'created_by_user', 'created_at']),
            models.Index(fields=['id', 'chat_source', 'created_by_user', 'updated_at']),
            models.Index(fields=['id', 'chat_source', 'created_at', 'updated_at']),
            models.Index(fields=['id', 'is_archived', 'created_by_user', 'created_at']),
            models.Index(fields=['id', 'is_archived', 'created_by_user', 'updated_at']),
            models.Index(fields=['id', 'is_archived', 'created_at', 'updated_at']),
            models.Index(fields=['id', 'created_by_user', 'created_at', 'updated_at']),
            models.Index(fields=['organization', 'assistant', 'user', 'chat_source']),
            models.Index(fields=['organization', 'assistant', 'user', 'is_archived']),
            models.Index(fields=['organization', 'assistant', 'user', 'created_by_user']),
            models.Index(fields=['organization', 'assistant', 'user', 'created_at']),
            models.Index(fields=['organization', 'assistant', 'user', 'updated_at']),
            models.Index(fields=['organization', 'assistant', 'chat_source', 'is_archived']),
            models.Index(fields=['organization', 'assistant', 'chat_source', 'created_by_user']),
            models.Index(fields=['organization', 'assistant', 'chat_source', 'created_at']),
            models.Index(fields=['organization', 'assistant', 'chat_source', 'updated_at']),
            models.Index(fields=['organization', 'assistant', 'is_archived', 'created_by_user']),
            models.Index(fields=['organization', 'assistant', 'is_archived', 'created_at']),
            models.Index(fields=['organization', 'assistant', 'is_archived', 'updated_at']),
            models.Index(fields=['organization', 'assistant', 'created_by_user', 'created_at']),
            models.Index(fields=['organization', 'assistant', 'created_by_user', 'updated_at']),
            models.Index(fields=['organization', 'assistant', 'created_at', 'updated_at']),
            models.Index(fields=['organization', 'user', 'chat_source', 'is_archived']),
            models.Index(fields=['organization', 'user', 'chat_source', 'created_by_user']),
            models.Index(fields=['organization', 'user', 'chat_source', 'created_at']),
            models.Index(fields=['organization', 'user', 'chat_source', 'updated_at']),
            models.Index(fields=['organization', 'user', 'is_archived', 'created_by_user']),
            models.Index(fields=['organization', 'user', 'is_archived', 'created_at']),
            models.Index(fields=['organization', 'user', 'is_archived', 'updated_at']),
            models.Index(fields=['organization', 'user', 'created_by_user', 'created_at']),
            models.Index(fields=['organization', 'user', 'created_by_user', 'updated_at']),
            models.Index(fields=['organization', 'user', 'created_at', 'updated_at']),
            models.Index(fields=['organization', 'chat_source', 'is_archived', 'created_by_user']),
            models.Index(fields=['organization', 'chat_source', 'is_archived', 'created_at']),
            models.Index(fields=['organization', 'chat_source', 'is_archived', 'updated_at']),
            models.Index(fields=['organization', 'chat_source', 'created_by_user', 'created_at']),
            models.Index(fields=['organization', 'chat_source', 'created_by_user', 'updated_at']),
            models.Index(fields=['organization', 'chat_source', 'created_at', 'updated_at']),
            models.Index(fields=['organization', 'is_archived', 'created_by_user', 'created_at']),
            models.Index(fields=['organization', 'is_archived', 'created_by_user', 'updated_at']),
            models.Index(fields=['organization', 'is_archived', 'created_at', 'updated_at']),
            models.Index(fields=['organization', 'created_by_user', 'created_at', 'updated_at']),
            models.Index(fields=['assistant', 'user', 'chat_source', 'is_archived']),
            models.Index(fields=['assistant', 'user', 'chat_source', 'created_by_user']),
            models.Index(fields=['assistant', 'user', 'chat_source', 'created_at']),
            models.Index(fields=['assistant', 'user', 'chat_source', 'updated_at']),
            models.Index(fields=['assistant', 'user', 'is_archived', 'created_by_user']),
            models.Index(fields=['assistant', 'user', 'is_archived', 'created_at']),
            models.Index(fields=['assistant', 'user', 'is_archived', 'updated_at']),
            models.Index(fields=['assistant', 'user', 'created_by_user', 'created_at']),
            models.Index(fields=['assistant', 'user', 'created_by_user', 'updated_at']),
            models.Index(fields=['assistant', 'user', 'created_at', 'updated_at']),
            models.Index(fields=['assistant', 'chat_source', 'is_archived', 'created_by_user']),
            models.Index(fields=['assistant', 'chat_source', 'is_archived', 'created_at']),
            models.Index(fields=['assistant', 'chat_source', 'is_archived', 'updated_at']),
            models.Index(fields=['assistant', 'chat_source', 'created_by_user', 'created_at']),
            models.Index(fields=['assistant', 'chat_source', 'created_by_user', 'updated_at']),
            models.Index(fields=['assistant', 'chat_source', 'created_at', 'updated_at']),
            models.Index(fields=['assistant', 'is_archived', 'created_by_user', 'created_at']),
            models.Index(fields=['assistant', 'is_archived', 'created_by_user', 'updated_at']),
            models.Index(fields=['assistant', 'is_archived', 'created_at', 'updated_at']),
            models.Index(fields=['assistant', 'created_by_user', 'created_at', 'updated_at']),
            models.Index(fields=['user', 'chat_source', 'is_archived', 'created_by_user']),
            models.Index(fields=['user', 'chat_source', 'is_archived', 'created_at']),
            models.Index(fields=['user', 'chat_source', 'is_archived', 'updated_at']),
            models.Index(fields=['user', 'chat_source', 'created_by_user', 'created_at']),
            models.Index(fields=['user', 'chat_source', 'created_by_user', 'updated_at']),
            models.Index(fields=['user', 'chat_source', 'created_at', 'updated_at']),
            models.Index(fields=['user', 'is_archived', 'created_by_user', 'created_at']),
            models.Index(fields=['user', 'is_archived', 'created_by_user', 'updated_at']),
            models.Index(fields=['user', 'is_archived', 'created_at', 'updated_at']),
            models.Index(fields=['user', 'created_by_user', 'created_at', 'updated_at']),
            models.Index(fields=['chat_source', 'is_archived', 'created_by_user', 'created_at']),
            models.Index(fields=['chat_source', 'is_archived', 'created_by_user', 'updated_at']),
            models.Index(fields=['chat_source', 'is_archived', 'created_at', 'updated_at']),
            models.Index(fields=['chat_source', 'created_by_user', 'created_at', 'updated_at']),
            models.Index(fields=['is_archived', 'created_by_user', 'created_at', 'updated_at']),

        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Create the knowledge base connection in the ORM
        if (self.assistant.context_overflow_strategy == ContextOverflowStrategyNames.VECTORIZE
            and self.context_memory_connection is None):
            if self.assistant.vectorizer_name is None:
                print("[MultimodalChat.save] The assistant does not have a vectorizer name set.")
                return
            if self.assistant.vectorizer_api_key is None:
                print("[MultimodalChat.save] The assistant does not have a vectorizer API key set.")
                return
            context_history = ContextHistoryKnowledgeBaseConnection.objects.create(
                assistant=self.assistant, chat=self, vectorizer=self.assistant.vectorizer_name,
                vectorizer_api_key=self.assistant.vectorizer_api_key
            )
            # Create the Weaviate classes for the context chat history memory
            connection = ContextHistoryKnowledgeBaseConnection.objects.get(id=context_history.id)
            self.context_memory_connection = connection
            self.save()

    def delete(self, using=None, keep_parents=False):
        # Remove the context memory connection
        if self.context_memory_connection:
            executor = MemoryExecutor(connection=self.context_memory_connection)
            executor.delete_chat_history_classes(class_name=self.context_memory_connection.class_name)
            self.context_memory_connection.delete()
        super().delete(using, keep_parents)
