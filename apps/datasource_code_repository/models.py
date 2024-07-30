import os

from django.db import models
from slugify import slugify

from apps._services.code_repository.code_repository_decoder import CodeRepositorySystemDecoder
from apps.datasource_code_repository.utils import generate_class_name
from apps.datasource_knowledge_base.models import KNOWLEDGE_BASE_SYSTEMS

# Create your models here.


VECTORIZERS = [
    ("text2vec-openai", "Text2Vec (OpenAI)"),
]


class CodeRepositoryConnection(models.Model):
    # Main information
    provider = models.CharField(max_length=100, choices=KNOWLEDGE_BASE_SYSTEMS, default="weaviate")
    host_url = models.CharField(max_length=1000, null=True, blank=True)
    provider_api_key = models.CharField(max_length=1000, null=True, blank=True)
    assistant = models.ForeignKey('assistants.Assistant', on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)

    git_clone_url = models.CharField(max_length=5000)
    git_username = models.CharField(max_length=1000)
    git_password = models.CharField(max_length=1000)

    # Class metadata
    class_name = models.CharField(max_length=1000, null=True, blank=True)
    description = models.TextField()
    vectorizer = models.CharField(max_length=100, choices=VECTORIZERS, default="text2vec-openai", null=True, blank=True)
    vectorizer_api_key = models.CharField(max_length=1000, null=True, blank=True)

    # Langchain chunking rules
    embedding_chunk_size = models.IntegerField(default=1024)
    embedding_chunk_overlap = models.IntegerField(default=256)

    # Schema (for defining the overall structure to the assistant)
    schema_json = models.TextField(null=True, blank=True)

    # Code repositories have chunks
    code_repository_chunks = models.ManyToManyField(
        "CodeRepositoryChunk",
        related_name='repositories',
        blank=True)

    search_instance_retrieval_limit = models.IntegerField(default=10)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " - " + self.assistant.name + " - " + self.created_at.strftime("%Y%m%d%H%M%S")

    class Meta:
        verbose_name = "Code Repository Connection"
        verbose_name_plural = "Code Repository Connections"
        ordering = ["-created_at"]
        unique_together = ['assistant', 'name']
        indexes = [
            models.Index(fields=["assistant", "name"]),
            models.Index(fields=["assistant", "created_at"]),
            models.Index(fields=["assistant", "updated_at"]),
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

        client = CodeRepositorySystemDecoder.get(self)
        if client is not None:
            result = client.create_weaviate_classes()
            if not result["status"]:
                raise Exception(f"Error creating Code Repository Weaviate class: {result['error']}")

        self.schema_json = client.retrieve_schema()
        super().save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        # Delete the class from Weaviate
        client = CodeRepositorySystemDecoder.get(self)
        if client is not None:
            result = client.delete_weaviate_classes(class_name=self.class_name)
            if not result["status"]:
                raise Exception(f"Error deleting Code Repository Weaviate class: {result['error']}")

        super().delete(using, keep_parents)


class CodeRepositoryChunk(models.Model):
    code_repository_connection = models.ForeignKey("CodeRepositoryConnection", on_delete=models.CASCADE)

    document_file_name = models.CharField(max_length=1000)
    document_description = models.TextField()  # null for now
    document_metadata = models.JSONField()  # auto
    document_uri = models.CharField(max_length=1000, null=True, blank=True)

    # to associate the element with the Weaviate object
    code_repo_uuid = models.CharField(max_length=1000, null=True, blank=True)

    # Documents have chunks
    document_content_temporary = models.TextField(blank=True, null=True)  # This will be emptied before indexing

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return slugify(self.document_file_name) + " - " + self.code_repository_connection.name + " - " + str(
            self.code_repository_connection.id)

    class Meta:
        verbose_name = "Code Repository Chunk"
        verbose_name_plural = "Code Repository Chunks"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["code_repository_connection", "document_file_name"]),
            models.Index(fields=["code_repository_connection", "created_at"]),
            models.Index(fields=["code_repository_connection", "updated_at"]),
        ]

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.document_file_name = slugify(self.document_file_name)
        self.document_content_temporary = ""
        self.document_description = ""
        super().save(force_insert, force_update, using, update_fields)


class CodeFileUploadStatusNames:
    STAGED = 'staged'
    UPLOADED = 'uploaded'
    LOADED = 'loaded'
    CHUNKED = 'chunked'
    EMBEDDED_DOCUMENT = 'embedded_document'
    SAVED_DOCUMENT = 'saved_document'
    PROCESSED_DOCUMENT = 'processed_document'
    EMBEDDED_CHUNKS = 'embedded_chunks'
    SAVED_CHUNKS = 'saved_chunks'
    PROCESSED_CHUNKS = 'processed_chunks'
    COMPLETED = 'completed'
    FAILED = 'failed'
    PARTIALLY_FAILED = 'partially_failed'


class CodeFileProcessingLog(models.Model):
    document_full_uri = models.CharField(max_length=4000)
    log_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.document_full_uri + " - " + self.created_at.strftime("%Y%m%d%H%M%S")

    class Meta:
        verbose_name = "Code File Processing Log"
        verbose_name_plural = "Code File Processing Logs"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["document_full_uri"]),
            models.Index(fields=["created_at"]),
        ]
