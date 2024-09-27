from django.db import models

from apps._services.knowledge_base.memory.memory_executor import MemoryExecutor
from apps.datasource_knowledge_base.utils import VECTORIZERS, generate_chat_history_class_name


class ContextHistoryKnowledgeBaseConnection(models.Model):
    """
    ContextHistoryKnowledgeBaseConnection Model:
    - Purpose: Represents a connection to a context history knowledge base, storing metadata and configuration settings related to memory management and embedding.
    - Key Fields:
        - `assistant`: ForeignKey linking to the `Assistant` model.
        - `chat`: ForeignKey linking to the `MultimodalChat` model.
        - `class_name`: Metadata field for the class name.
        - `vectorizer`, `vectorizer_api_key`: Configuration for the vectorizer used in context history embedding.
        - `context_history_memories`: ManyToManyField linking to the memories in the context history.
        - `created_at`, `updated_at`: Timestamps for creation and last update.
    - Methods:
        - `save()`: Overridden to handle vectorizer defaults, generate class names, and interact with the context history system for class creation.
        - `delete()`: Overridden to remove related classes from the context history system.
    """

    assistant = models.ForeignKey('assistants.Assistant', on_delete=models.CASCADE, default=1)
    chat = models.ForeignKey('multimodal_chat.MultimodalChat', on_delete=models.CASCADE, default=1)

    class_name = models.CharField(max_length=1000, null=True, blank=True)
    vectorizer = models.CharField(max_length=100, choices=VECTORIZERS, default="text2vec-openai")
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

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.vectorizer is None:
            self.vectorizer = "text2vec-openai"
        if self.class_name is None:
            self.class_name = generate_chat_history_class_name()
        super().save(force_insert, force_update, using, update_fields)

        client = MemoryExecutor(connection=self)
        if client is not None:
            result = client.create_chat_history_classes()
            if not result["status"]:
                print(
                    f"[ContextHistoryKnowledgeBaseConnection.save] Error creating Chat History class: {result['error']}")

    def delete(self, using=None, keep_parents=False):
        # delete the classes from Weaviate
        client = MemoryExecutor(connection=self)
        if client is not None:
            result = client.delete_chat_history_classes(class_name=self.class_name)
            if not result["status"]:
                print(
                    f"[ContextHistoryKnowledgeBaseConnection.delete] Error deleting Chat History class: {result['error']}")
        super().delete(using, keep_parents)
