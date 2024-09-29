#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: document_chunk_models.py
#  Last Modified: 2024-09-26 22:02:31
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:42:36
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.db import models

from apps.datasource_knowledge_base.utils import SUPPORTED_DOCUMENT_TYPES


class KnowledgeBaseDocumentChunk(models.Model):
    """
    KnowledgeBaseDocumentChunk Model:
    - Purpose: Represents a chunk of a document within a knowledge base, storing information about the chunk's content, metadata, and its association with the document and knowledge base.
    - Key Fields:
        - `knowledge_base`: ForeignKey linking to the `DocumentKnowledgeBaseConnection` model.
        - `document`: ForeignKey linking to the `KnowledgeBaseDocument` model.
        - `chunk_document_type`: The type of document chunk (e.g., PDF, HTML).
        - `chunk_number`: The sequence number of the chunk.
        - `chunk_content`, `chunk_metadata`, `chunk_document_uri`: Fields for storing the chunk's content and metadata.
        - `knowledge_base_uuid`, `document_uuid`: UUIDs for linking the chunk to the knowledge base and document.
        - `created_at`, `updated_at`: Timestamps for creation and last update.
    """

    knowledge_base = models.ForeignKey("DocumentKnowledgeBaseConnection", on_delete=models.CASCADE)
    document = models.ForeignKey("KnowledgeBaseDocument", on_delete=models.CASCADE,
                                 related_name='document_chunks')

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

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
