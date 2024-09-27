from django.db import models

from apps._services.knowledge_base.document.knowledge_base_decoder import KnowledgeBaseSystemDecoder
from apps.datasource_knowledge_base.utils import KNOWLEDGE_BASE_SYSTEMS, VECTORIZERS, generate_class_name


class DocumentKnowledgeBaseConnection(models.Model):
    """
    DocumentKnowledgeBaseConnection Model:
    - Purpose: Represents a connection to a knowledge base system, storing metadata and configuration settings related to document management and embedding.
    - Key Fields:
        - `provider`: The knowledge base system provider (e.g., Weaviate).
        - `host_url`: The URL of the knowledge base system.
        - `provider_api_key`: API key for the provider.
        - `assistant`: ForeignKey linking to the `Assistant` model.
        - `name`, `class_name`, `description`: Metadata fields for the knowledge base connection.
        - `vectorizer`, `vectorizer_api_key`: Configuration for the vectorizer used in document embedding.
        - `embedding_chunk_size`, `embedding_chunk_overlap`: Parameters for document chunking.
        - `schema_json`: JSON schema for the knowledge base structure.
        - `knowledge_base_documents`: ManyToManyField linking to the documents in the knowledge base.
        - `search_instance_retrieval_limit`: Limit on the number of search instances.
        - `created_at`, `updated_at`: Timestamps for creation and last update.
    - Methods:
        - `save()`: Overridden to handle vectorizer defaults, generate class names, and interact with the knowledge base system for class creation.
        - `delete()`: Overridden to remove related classes from the knowledge base system.
    """

    # Main information
    provider = models.CharField(max_length=100, choices=KNOWLEDGE_BASE_SYSTEMS)
    host_url = models.CharField(max_length=1000)
    provider_api_key = models.CharField(max_length=1000, null=True, blank=True)
    assistant = models.ForeignKey('assistants.Assistant', on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)

    # Class metadata
    class_name = models.CharField(max_length=1000, null=True, blank=True)
    description = models.TextField()
    vectorizer = models.CharField(max_length=100, choices=VECTORIZERS, default="text2vec-openai", null=True,
                                  blank=True)
    vectorizer_api_key = models.CharField(max_length=1000, null=True, blank=True)

    # Langchain chunking rules
    embedding_chunk_size = models.IntegerField(default=1024)
    embedding_chunk_overlap = models.IntegerField(default=256)

    # Schema (for defining the overall structure to the assistant)
    schema_json = models.TextField(null=True, blank=True)

    search_instance_retrieval_limit = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " - " + self.assistant.name + " - " + self.created_at.strftime("%Y%m%d%H%M%S")

    class Meta:
        verbose_name = "Document Knowledge Base Connection"
        verbose_name_plural = "Document Knowledge Base Connections"
        ordering = ["-created_at"]
        unique_together = ['host_url', 'assistant']
        indexes = [
            models.Index(fields=["provider", "assistant", "name"]),
            models.Index(fields=["provider", "assistant", "created_at"]),
            models.Index(fields=["provider", "assistant", "updated_at"]),
            models.Index(fields=["class_name"]),
            models.Index(fields=["vectorizer"]),
        ]

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.vectorizer is None:
            self.vectorizer = "text2vec-openai"

        if self.class_name is None:
            self.class_name = generate_class_name(self)

        client = KnowledgeBaseSystemDecoder.get(self)
        if client is not None:
            result = client.create_weaviate_classes()
            if not result["status"]:
                print(f"[DocumentKnowledgeBaseConnection.save] Error creating Weaviate classes: {result['error']}")

        self.schema_json = client.retrieve_schema()
        super().save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        # delete the classes from Weaviate
        client = KnowledgeBaseSystemDecoder.get(self)
        if client is not None:
            result = client.delete_weaviate_classes(class_name=self.class_name)
            if not result["status"]:
                print(f"[DocumentKnowledgeBaseConnection.save] Error deleting Weaviate classes: {result['error']}")

        super().delete(using, keep_parents)
