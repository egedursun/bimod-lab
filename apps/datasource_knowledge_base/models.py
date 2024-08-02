import os

from django.db import models
from slugify import slugify

from apps._services.knowledge_base.document.knowledge_base_decoder import KnowledgeBaseSystemDecoder
from apps._services.knowledge_base.memory.memory_executor import MemoryExecutor
from apps.assistants.models import VECTORIZERS
from apps.datasource_knowledge_base.utils import generate_class_name, generate_random_alphanumeric, \
    generate_chat_history_class_name

# Create your models here.

KNOWLEDGE_BASE_SYSTEMS = [
    ('weaviate', 'Weaviate'),
]


class KnowledgeBaseSystemNames:
    WEAVIATE = 'weaviate'


SUPPORTED_DOCUMENT_TYPES = [
    ('pdf', 'PDF'),
    ('html', 'HTML'),
    ('csv', 'CSV'),
    ('docx', 'DOCX'),
    ('ipynb', 'IPYNB'),
    ('json', 'JSON'),
    ('xml', 'XML'),
    ('txt', 'TXT'),
    ('md', 'MD'),
    ('rtf', 'RTF'),
    ('odt', 'ODT'),
    ('pptx', 'POWERPOINT'),
    ('xlsx', 'XLSX')
]


class SupportedDocumentTypesNames:
    PDF = 'pdf'
    HTML = 'html'
    CSV = 'csv'
    DOCX = 'docx'
    IPYNB = 'ipynb'
    JSON = 'json'
    XML = 'xml'
    TXT = 'txt'
    MD = 'md'
    RTF = 'rtf'
    ODT = 'odt'
    POWERPOINT = 'pptx'
    XLSX = 'xlsx'


class DocumentKnowledgeBaseConnection(models.Model):
    # Main information
    provider = models.CharField(max_length=100, choices=KNOWLEDGE_BASE_SYSTEMS)
    host_url = models.CharField(max_length=1000)
    provider_api_key = models.CharField(max_length=1000, null=True, blank=True)
    assistant = models.ForeignKey('assistants.Assistant', on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)

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

    # Knowledge bases have documents
    knowledge_base_documents = models.ManyToManyField("KnowledgeBaseDocument", related_name='knowledge_bases',
                                                      blank=True)

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
                print(f"Error creating Weaviate classes: {result['error']}")

        self.schema_json = client.retrieve_schema()
        super().save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        # delete the classes from Weaviate
        client = KnowledgeBaseSystemDecoder.get(self)
        if client is not None:
            result = client.delete_weaviate_classes(class_name=self.class_name)
            if not result["status"]:
                print(f"Error deleting Weaviate classes: {result['error']}")

        super().delete(using, keep_parents)


class KnowledgeBaseDocument(models.Model):
    knowledge_base = models.ForeignKey("DocumentKnowledgeBaseConnection", on_delete=models.CASCADE,
                                       related_name='documents')

    document_type = models.CharField(max_length=100, choices=SUPPORTED_DOCUMENT_TYPES)  # auto
    document_file_name = models.CharField(max_length=1000)
    document_description = models.TextField()  # null for now
    document_metadata = models.JSONField()  # auto
    document_uri = models.CharField(max_length=1000, null=True, blank=True)

    # to associate the element with the Weaviate object
    knowledge_base_uuid = models.CharField(max_length=1000, null=True, blank=True)

    # Documents have chunks
    document_content_temporary = models.TextField(blank=True, null=True)  # This will be emptied before indexing
    document_chunks = models.ManyToManyField("KnowledgeBaseDocumentChunk", related_name='documents', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return slugify(self.document_file_name) + " - " + self.knowledge_base.name + " - " + str(
            self.knowledge_base.id)

    class Meta:
        verbose_name = "Knowledge Base Document"
        verbose_name_plural = "Knowledge Base Documents"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["knowledge_base", "document_file_name"]),
            models.Index(fields=["knowledge_base", "created_at"]),
            models.Index(fields=["knowledge_base", "updated_at"]),
        ]

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.document_file_name = slugify(self.document_file_name)
        self.document_content_temporary = ""
        self.document_description = ""
        super().save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        # delete the document from Weaviate
        client = KnowledgeBaseSystemDecoder.get(self.knowledge_base)
        if client is not None:
            result = client.delete_weaviate_document(
                class_name=self.knowledge_base.class_name,
                document_uuid=self.knowledge_base_uuid)
            if not result["status"]:
                print(f"Error deleting Weaviate document: {result['error']}")
            # remove the document from the directory
            document_full_path = self.document_uri
            if document_full_path is not None:
                try:
                    os.remove(document_full_path)
                except Exception as e:
                    print(f"Error deleting the document file: {e}")
        # delete the object from ORM
        super().delete(using, keep_parents)


class KnowledgeBaseDocumentChunk(models.Model):
    knowledge_base = models.ForeignKey("DocumentKnowledgeBaseConnection", on_delete=models.CASCADE)
    document = models.ForeignKey("KnowledgeBaseDocument", on_delete=models.CASCADE, related_name='chunks')

    chunk_document_type = models.CharField(max_length=100, choices=SUPPORTED_DOCUMENT_TYPES, blank=True, null=True)
    chunk_number = models.IntegerField()
    chunk_content = models.TextField()  # This will be the text content of the chunk
    chunk_metadata = models.TextField()
    chunk_document_uri = models.CharField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    knowledge_base_uuid = models.CharField(max_length=1000, null=True, blank=True)
    document_uuid = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return str(
            self.chunk_number) + " - " + self.document.document_file_name + " - " + self.document.knowledge_base.name

    class Meta:
        verbose_name = "Knowledge Base Document Chunk"
        verbose_name_plural = "Knowledge Base Document Chunks"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["knowledge_base", "document", "chunk_number"]),
            models.Index(fields=["knowledge_base", "document", "created_at"]),
            models.Index(fields=["knowledge_base", "document", "updated_at"]),
        ]

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save(force_insert, force_update, using, update_fields)


class ContextHistoryKnowledgeBaseConnection(models.Model):
    assistant = models.ForeignKey('assistants.Assistant', on_delete=models.CASCADE, default=1)
    chat = models.ForeignKey('multimodal_chat.MultimodalChat', on_delete=models.CASCADE, default=1)

    class_name = models.CharField(max_length=1000, null=True, blank=True)
    vectorizer = models.CharField(max_length=100, choices=VECTORIZERS, default="text2vec-openai")
    vectorizer_api_key = models.CharField(max_length=1000, null=True, blank=True)

    # Knowledge bases have memories
    context_history_memories = models.ManyToManyField("ContextHistoryMemory", related_name='knowledge_bases',
                                                      blank=True)

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
                print(f"Error creating Chat History class: {result['error']}")

    def delete(self, using=None, keep_parents=False):
        # delete the classes from Weaviate
        client = MemoryExecutor(connection=self)
        if client is not None:
            result = client.delete_chat_history_classes(class_name=self.class_name)
            if not result["status"]:
                print(f"Error deleting Chat History class: {result['error']}")

        super().delete(using, keep_parents)


class ContextHistoryMemory(models.Model):
    context_history_base = models.ForeignKey("ContextHistoryKnowledgeBaseConnection", on_delete=models.CASCADE,
                                             related_name='memories')
    memory_name = models.CharField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # to associate the element with the Weaviate object
    knowledge_base_memory_uuid = models.CharField(max_length=1000, null=True, blank=True)

    memory_chunks = models.ManyToManyField("ContextHistoryMemoryChunk", related_name='memories', blank=True)

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
                print(f"Error deleting Weaviate document: {result['error']}")
        # delete the object from ORM
        super().delete(using, keep_parents)


class ContextHistoryMemoryChunk(models.Model):
    context_history_base = models.ForeignKey("ContextHistoryKnowledgeBaseConnection", on_delete=models.CASCADE)
    memory = models.ForeignKey("ContextHistoryMemory", on_delete=models.CASCADE, related_name='chunks')

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


DOCUMENT_UPLOAD_STATUS = [
    ('staged', 'Staged'),
    ('uploaded', 'Uploaded'),
    ('loaded', 'Loaded'),
    ('chunked', 'Chunked'),
    ('embedded_document', 'Embedded Document'),
    ('saved_document', 'Saved Document'),
    ('processed_document', 'Processed Document'),
    ('embedded_chunks', 'Embedded Chunks'),
    ('saved_chunks', 'Saved Chunks'),
    ('processed_chunks', 'Processed Chunks'),
    ('completed', 'Completed'),
    ('failed', 'Failed'),
    ('partially_failed', 'Partially Failed')
]


class DocumentUploadStatusNames:
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


class DocumentProcessingLog(models.Model):
    document_full_uri = models.CharField(max_length=1000)
    log_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.document_full_uri + " - " + self.created_at.strftime("%Y%m%d%H%M%S")

    class Meta:
        verbose_name = "Document Processing Log"
        verbose_name_plural = "Document Processing Logs"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["document_full_uri"]),
            models.Index(fields=["created_at"]),
        ]
