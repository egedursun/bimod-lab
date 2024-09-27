import os

import boto3
from django.db import models
from slugify import slugify

from apps._services.knowledge_base.document.knowledge_base_decoder import KnowledgeBaseSystemDecoder
from apps.datasource_knowledge_base.utils import SUPPORTED_DOCUMENT_TYPES
from config.settings import MEDIA_URL


class KnowledgeBaseDocument(models.Model):
    """
    KnowledgeBaseDocument Model:
    - Purpose: Represents a document within a knowledge base, storing information about the document type, file name, metadata, and its association with the knowledge base.
    - Key Fields:
        - `knowledge_base`: ForeignKey linking to the `DocumentKnowledgeBaseConnection` model.
        - `document_type`: The type of document (e.g., PDF, HTML).
        - `document_file_name`, `document_description`, `document_metadata`, `document_uri`: Metadata fields for the document.
        - `knowledge_base_uuid`: UUID for linking the document to the knowledge base system.
        - `document_content_temporary`: Temporary storage for document content before indexing.
        - `document_chunks`: ManyToManyField linking to the document chunks.
        - `created_at`, `updated_at`: Timestamps for creation and last update.
    - Methods:
        - `save()`: Overridden to handle file name slugification and content clearing before saving.
        - `delete()`: Overridden to remove the document from the knowledge base system and delete the associated file.
    """

    knowledge_base = models.ForeignKey("DocumentKnowledgeBaseConnection", on_delete=models.CASCADE,
                                       related_name='knowledge_base_documents')

    document_type = models.CharField(max_length=100, choices=SUPPORTED_DOCUMENT_TYPES)  # auto
    document_file_name = models.CharField(max_length=1000)
    document_description = models.TextField()  # null for now
    document_metadata = models.JSONField()  # auto
    document_uri = models.CharField(max_length=1000, null=True, blank=True)

    # to associate the element with the Weaviate object
    knowledge_base_uuid = models.CharField(max_length=1000, null=True, blank=True)

    # Documents have chunks
    document_content_temporary = models.TextField(blank=True, null=True)  # This will be emptied before indexing

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
                print(f"[KnowledgeBaseDocument.delete] Error deleting Weaviate document: {result['error']}")
            # remove the document from the S3 bucket (will give the absolute path)
            document_full_path = self.document_uri
            boto3_client = boto3.client('s3')
            bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
            s3_path = document_full_path.split(MEDIA_URL)[1]
            s3_path = s3_path.replace('/', '')
            s3_path = f"{s3_path}/"
            if document_full_path is not None:
                try:
                    boto3_client.delete_object(Bucket=bucket_name, Key=s3_path)
                except Exception as e:
                    print(f"[KnowledgeBaseDocument.delete] Error deleting S3 object: {str(e)}")
        # delete the object from ORM
        super().delete(using, keep_parents)
