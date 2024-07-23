import os

from django.db import models
from slugify import slugify

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
    git_clone_url = models.CharField(max_length=5000)
    git_username = models.CharField(max_length=1000)
    git_password = models.CharField(max_length=1000)

    name = models.CharField(max_length=1000)
    description = models.TextField()

    # Class metadata
    class_name = models.CharField(max_length=1000, null=True, blank=True)
    vectorizer = models.CharField(max_length=100, choices=VECTORIZERS, default="text2vec-openai",
                                  null=True, blank=True)
    vectorizer_api_key = models.CharField(max_length=1000, null=True, blank=True)

    # Langchain chunking rules
    embedding_chunk_size = models.IntegerField(default=1024)
    embedding_chunk_overlap = models.IntegerField(default=256)

    # Schema (for defining the overall structure to the assistant)
    schema_json = models.TextField(null=True, blank=True)

    # Code repositories have files
    code_repository_files = models.ManyToManyField(
        "CodeRepositoryFile",
        related_name='code_repository',
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

        # TODO-1: Implement the creation of the Weaviate classes
        client = None  # KnowledgeBaseSystemDecoder.get(self)
        if client is not None:
            result = None  # client.create_weaviate_classes()
            #  if not result["status"]:
            #      print(f"Error creating Weaviate classes: {result['error']}")
            pass

        self.schema_json = None  # client.retrieve_schema()
        super().save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        # TODO-2: Implement the deletion of the Weaviate classes
        # delete the classes from Weaviate
        client = None  # KnowledgeBaseSystemDecoder.get(self)
        if client is not None:
            result = None  # client.delete_weaviate_classes(class_name=self.class_name)
            #  if not result["status"]:
            #      print(f"Error deleting Weaviate classes: {result['error']}")

        super().delete(using, keep_parents)


class CodeRepositoryFile(models.Model):
    code_repository_connection = models.ForeignKey("CodeRepositoryConnection", on_delete=models.CASCADE)

    document_file_name = models.CharField(max_length=1000)
    document_description = models.TextField()  # null for now
    document_metadata = models.JSONField()  # auto
    document_uri = models.CharField(max_length=1000, null=True, blank=True)

    # to associate the element with the Weaviate object
    code_repo_uuid = models.CharField(max_length=1000, null=True, blank=True)

    # Documents have chunks
    document_content_temporary = models.TextField(blank=True, null=True)  # This will be emptied before indexing
    document_chunks = models.ManyToManyField("CodeRepositoryFileChunk", related_name='files', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return slugify(self.document_file_name) + " - " + self.code_repository_connection.name + " - " + str(
            self.code_repository_connection.id)

    class Meta:
        verbose_name = "Code Repository File"
        verbose_name_plural = "Code Repository Files"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["code_repository_connection", "document_file_name"]),
            models.Index(fields=["code_repository_connection", "created_at"]),
            models.Index(fields=["code_repository_connection", "updated_at"]),
        ]

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.document_file_name = slugify(self.document_file_name)
        self.document_content_temporary = ""
        self.document_description = ""
        super().save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        # TODO-3: Implement the deletion of the Weaviate documents
        # delete the document from Weaviate
        client = None  # KnowledgeBaseSystemDecoder.get(self.knowledge_base)
        if client is not None:
            result = None  # client.delete_weaviate_document(class_name=self.knowledge_base.class_name, document_uuid=self.knowledge_base_uuid)
            #  if not result["status"]:
            #      print(f"Error deleting Weaviate document: {result['error']}")
            # remove the document from the directory
            document_full_path = self.document_uri
            if document_full_path is not None:
                try:
                    os.remove(document_full_path)
                except Exception as e:
                    print(f"Error deleting the document file: {e}")
        # delete the object from ORM
        super().delete(using, keep_parents)


class CodeRepositoryFileChunk(models.Model):
    code_repository_connection = models.ForeignKey("CodeRepositoryConnection", on_delete=models.CASCADE)
    file = models.ForeignKey("CodeRepositoryFile", on_delete=models.CASCADE, related_name='chunks')

    chunk_number = models.IntegerField()
    chunk_content = models.TextField()  # This will be the text content of the chunk
    chunk_metadata = models.TextField()
    chunk_document_uri = models.CharField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    knowledge_base_uuid = models.CharField(max_length=1000, null=True, blank=True)
    document_uuid = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return (str(
            self.chunk_number) + " - " + self.file.document_file_name + " - " + self.code_repository_connection.name
                + " - " + str(self.code_repository_connection.id))

    class Meta:
        verbose_name = "Code Repository File Chunk"
        verbose_name_plural = "Code Repository File Chunks"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["code_repository_connection", "file", "chunk_number"]),
            models.Index(fields=["code_repository_connection", "file", "created_at"]),
            models.Index(fields=["code_repository_connection", "file", "updated_at"]),
        ]

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save(force_insert, force_update, using, update_fields)
