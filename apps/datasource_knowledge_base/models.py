from django.db import models

from apps._services.knowledge_base.document.knowledge_base_decoder import KnowledgeBaseSystemDecoder
from apps.assistants.models import VECTORIZERS
from apps.datasource_knowledge_base.utils import generate_class_name

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

###################################################################################################################


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
    vectorizer = models.CharField(max_length=100, choices=VECTORIZERS, default="text2vec-openai",
                                  null=True, blank=True)
    vectorizer_api_key = models.CharField(max_length=1000, null=True, blank=True)

    # Langchain chunking rules
    embedding_chunk_size = models.IntegerField(default=1024)
    embedding_chunk_overlap = models.IntegerField(default=256)

    # Schema (for defining the overall structure to the assistant)
    schema_json = models.TextField(null=True, blank=True)

    # Knowledge bases have documents
    knowledge_base_documents = models.ManyToManyField("KnowledgeBaseDocument", related_name='knowledge_bases', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " - " + self.assistant.name + " - " + self.created_at.strftime("%Y%m%d%H%M%S")

    class Meta:
        verbose_name = "Document Knowledge Base Connection"
        verbose_name_plural = "Document Knowledge Base Connections"
        ordering = ["-created_at"]
        unique_together = ['host_url', 'assistant']

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
        client = KnowledgeBaseSystemDecoder.get(self)
        if client is not None:
            result = client.delete_weaviate_classes(class_name=self.class_name)
            if not result["status"]:
                print(f"Error deleting Weaviate classes: {result['error']}")
        super().delete(using, keep_parents)


class KnowledgeBaseDocument(models.Model):
    knowledge_base = models.ForeignKey("DocumentKnowledgeBaseConnection", on_delete=models.CASCADE,
                                       related_name='documents')

    document_type = models.CharField(max_length=100, choices=SUPPORTED_DOCUMENT_TYPES)
    document_file_name = models.CharField(max_length=1000)
    document_description = models.TextField()
    document_metadata = models.JSONField()
    document_uri = models.CharField(max_length=1000, null=True, blank=True)

    # to associate the element with the Weaviate object
    knowledge_base_uuid = models.CharField(max_length=1000, null=True, blank=True)

    # Documents have chunks
    document_content_temporary = models.TextField(blank=True, null=True)  # This will be emptied before indexing
    document_chunks = models.ManyToManyField("KnowledgeBaseDocumentChunk", related_name='documents', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.document_file_name + " - " + self.knowledge_base.name + " - " + str(self.knowledge_base.id)

    class Meta:
        verbose_name = "Knowledge Base Document"
        verbose_name_plural = "Knowledge Base Documents"
        ordering = ["-created_at"]

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.document_content_temporary = None
        super().save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        client = KnowledgeBaseSystemDecoder.get(self.knowledge_base)
        if client is not None:
            result = client.delete_weaviate_document(
                class_name=self.knowledge_base.class_name,
                document_uuid=self.knowledge_base_uuid)
            if not result["status"]:
                print(f"Error deleting Weaviate document: {result['error']}")
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
        return str(self.chunk_number) + " - " + self.document.document_file_name + " - " + self.document.knowledge_base.name

    class Meta:
        verbose_name = "Knowledge Base Document Chunk"
        verbose_name_plural = "Knowledge Base Document Chunks"
        ordering = ["-created_at"]

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save(force_insert, force_update, using, update_fields)


###################################################################################################################


# [2A] TODO: A data model for a specific type of knowledge base, more concrete (for storing previous chats)
#       This will not be reached by the user, therefore will have no 'templates', but it will be used
#       by the assistants if the strategy for vectorization has been selected.


# [2B] TODO: The data model for the objects stored in the knowledge base as memories


###################################################################################################################


# [3A] TODO: A data model for a specific type of knowledge base, more concrete (for storing browsed web pages)
#       This will not be reached by the user, therefore will have no 'templates', but it will be used
#       by the assistants if the strategy for vectorization has been selected.


# [3B] TODO: A data model for the objects stored in the knowledge base as web pages

# [3C] TODO: A data model for the objects stored in the knowledge base as web page chunks


###################################################################################################################
