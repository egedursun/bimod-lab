"""
Module Overview: This module defines models related to multimodal chats within an assistant-based application. It includes models for managing chat sessions, messages, and related logs. The module also provides functionality for handling context memory, starred messages, and organization balance checks during chat interactions.

Dependencies:
- `django.db.models`: Django's ORM for defining database models.
- `apps._services.knowledge_base.memory.memory_executor.MemoryExecutor`: Used for managing context memory connections.
- `apps.assistants.models.ContextOverflowStrategyNames`: Contains constants related to context overflow strategies.
- `apps.datasource_knowledge_base.models.ContextHistoryKnowledgeBaseConnection`: Represents connections to context history knowledge bases.
- `apps.llm_transaction.models.LLMTransaction`: Model for managing transactions related to language model operations.
- `apps.starred_messages.models.StarredMessage`: Model for managing starred messages within chats.
"""

from django.db import models

from apps._services.knowledge_base.memory.memory_executor import MemoryExecutor
from apps.assistants.models import ContextOverflowStrategyNames
from apps.datasource_knowledge_base.models import ContextHistoryKnowledgeBaseConnection
from apps.llm_transaction.models import LLMTransaction
from apps.starred_messages.models import StarredMessage

CHAT_SOURCES = [
    ("app", "Application"),
    ("api", "API"),
    ("scheduled", "Scheduled"),
    ("orchestration", "Orchestration"),
]


class ChatSourcesNames:
    APP = "app"
    API = "api"
    SCHEDULED = "scheduled"
    TRIGGERED = "triggered"
    ORCHESTRATION = "orchestration"


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
                                  related_name='multimodal_chats', default=1)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='multimodal_chats', default=1)
    chat_name = models.CharField(max_length=255)
    created_by_user = models.ForeignKey('auth.User', on_delete=models.CASCADE,
                                        related_name='multimodal_chats_created_by_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Chat Messages
    chat_messages = models.ManyToManyField('multimodal_chat.MultimodalChatMessage', related_name='multimodal_chats',
                                           blank=True)
    transactions = models.ManyToManyField('llm_transaction.LLMTransaction', related_name='multimodal_chats',
                                          blank=True)
    # Context Memory
    context_memory_connection = models.OneToOneField(ContextHistoryKnowledgeBaseConnection, on_delete=models.CASCADE,
                                                     related_name='multimodal_chat', null=True, blank=True)
    starred_messages = models.ManyToManyField('starred_messages.StarredMessage', related_name='multimodal_chats',
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


class MessageSenderTypeNames:
    USER = "USER"
    ASSISTANT = "ASSISTANT"
    SYSTEM = "SYSTEM"
    TOOL = "TOOL"


MESSAGE_SENDER_TYPES = [
    ("USER", "User"),
    ("ASSISTANT", "Assistant"),
    ("SYSTEM", "System"),
    ("TOOL", "Tool"),
]


class MultimodalChatMessage(models.Model):
    """
    MultimodalChatMessage Model:
    - Purpose: Represents a message within a multimodal chat session. It stores the message content, sender type, multimedia contents, and whether the message is starred. The model also provides methods for managing related transactions and starred messages.
    - Key Fields:
        - `multimodal_chat`: ForeignKey linking to the `MultimodalChat` model that this message belongs to.
        - `sender_type`: Field specifying the sender type (e.g., User, Assistant).
        - `message_text_content`: The textual content of the message.
        - `message_json_content`: JSON field for storing additional message content (not used currently).
        - `message_image_contents`: JSON field for storing image contents related to the message.
        - `message_file_contents`: JSON field for storing file contents related to the message.
        - `message_audio`: URL field for storing audio contents related to the message.
        - `starred`: Boolean field indicating whether the message is starred.
        - `sent_at`: Timestamp for when the message was sent.
    - Methods:
        - `get_organization_balance()`: Retrieves the current balance of the organization associated with the chat.
        - `token_cost_surpasses_the_balance(total_billable_cost)`: Checks if the token cost surpasses the organization's balance.
        - `save()`: Overridden to handle transactions, starred messages, and related logic when the message is saved.
    - Meta:
        - `verbose_name`: "Multimodal Chat Message"
        - `verbose_name_plural`: "Multimodal Chat Messages"
        - `ordering`: Orders messages by sent date in descending order.
        - `indexes`: Indexes on various fields for optimized queries.
    """

    multimodal_chat = models.ForeignKey('multimodal_chat.MultimodalChat', on_delete=models.CASCADE,
                                        related_name='messages_chat')
    sender_type = models.CharField(max_length=10, choices=MESSAGE_SENDER_TYPES)
    message_text_content = models.TextField()
    message_json_content = models.JSONField(default=dict, blank=True, null=True)  # Not used for now
    # Multimedia Contents
    message_image_contents = models.JSONField(default=list, blank=True, null=True)
    message_file_contents = models.JSONField(default=list, blank=True, null=True)
    # Narrated audio
    message_audio = models.URLField(max_length=10000, blank=True, null=True)

    starred = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.multimodal_chat.chat_name} - {self.sender_type} - {self.sent_at}"

    class Meta:
        verbose_name = "Multimodal Chat Message"
        verbose_name_plural = "Multimodal Chat Messages"
        ordering = ["-sent_at"]
        indexes = [
            # Single-field indexes
            models.Index(fields=['multimodal_chat']),
            models.Index(fields=['sender_type']),
            models.Index(fields=['starred']),
            models.Index(fields=['sent_at']),

            # Two-field composite indexes
            models.Index(fields=['multimodal_chat', 'sender_type']),
            models.Index(fields=['multimodal_chat', 'starred']),
            models.Index(fields=['multimodal_chat', 'sent_at']),
            models.Index(fields=['sender_type', 'starred']),
            models.Index(fields=['sender_type', 'sent_at']),
            models.Index(fields=['starred', 'sent_at']),

            # Three-field composite indexes
            models.Index(fields=['multimodal_chat', 'sender_type', 'starred']),
            models.Index(fields=['multimodal_chat', 'sender_type', 'sent_at']),
            models.Index(fields=['multimodal_chat', 'starred', 'sent_at']),
            models.Index(fields=['sender_type', 'starred', 'sent_at']),

            # Four-field composite indexes
            models.Index(fields=['multimodal_chat', 'sender_type', 'starred', 'sent_at']),
        ]

    def get_organization_balance(self):
        return self.multimodal_chat.organization.balance

    def token_cost_surpasses_the_balance(self, total_billable_cost):
        return self.multimodal_chat.organization.balance < total_billable_cost

    # create the transaction on save
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        MultimodalChat.objects.get(id=self.multimodal_chat.id).chat_messages.add(self.id)
        # if the message is starred, create the starred item
        if self.starred:
            if not self.multimodal_chat.starred_messages.filter(chat_message=self.id).exists():
                new_starred_message = StarredMessage.objects.create(
                    user=self.multimodal_chat.user, organization=self.multimodal_chat.organization,
                    assistant=self.multimodal_chat.assistant, chat=self.multimodal_chat,
                    chat_message=self, message_text=self.message_text_content, sender_type=self.sender_type
                )
                self.multimodal_chat.starred_messages.add(new_starred_message)
                self.multimodal_chat.save()
            else:
                pass
        else:
            # remove the starred item if it exists
            starred_message = StarredMessage.objects.filter(chat_message=self.id)
            if starred_message:
                starred_message.delete()


class ChatCreationLog(models.Model):
    """
    ChatCreationLog Model:
    - Purpose: Represents a log entry for the creation of a multimodal chat. It stores the organization associated with the chat and the timestamp of creation.
    - Key Fields:
        - `organization`: ForeignKey linking to the `Organization` model.
        - `created_at`: Timestamp for when the chat was created.
    - Meta:
        - `verbose_name`: "Chat Creation Log"
        - `verbose_name_plural`: "Chat Creation Logs"
        - `ordering`: Orders logs by creation date in descending order.
        - `indexes`: Indexes on the creation date for optimized queries.
    """

    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at}"

    class Meta:
        verbose_name = "Chat Creation Log"
        verbose_name_plural = "Chat Creation Logs"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['created_at']),
        ]


class ChatMessageCreationLog(models.Model):
    """
    ChatMessageCreationLog Model:
    - Purpose: Represents a log entry for the creation of a message within a multimodal chat. It stores the organization associated with the message and the timestamp of creation.
    - Key Fields:
        - `organization`: ForeignKey linking to the `Organization` model.
        - `created_at`: Timestamp for when the message was created.
    - Meta:
        - `verbose_name`: "Chat Message Creation Log"
        - `verbose_name_plural`: "Chat Message Creation Logs"
        - `ordering`: Orders logs by creation date in descending order.
        - `indexes`: Indexes on the creation date for optimized queries.
    """

    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at}"

    class Meta:
        verbose_name = "Chat Message Creation Log"
        verbose_name_plural = "Chat Message Creation Logs"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['created_at']),
        ]
