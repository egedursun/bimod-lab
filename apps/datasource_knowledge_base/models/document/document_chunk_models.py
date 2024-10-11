#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: document_chunk_models.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:47
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

from django.db import models

from apps.datasource_knowledge_base.utils import UPLOAD_FILES_SUPPORTED_FORMATS


class KnowledgeBaseDocumentChunk(models.Model):
    knowledge_base = models.ForeignKey("DocumentKnowledgeBaseConnection", on_delete=models.CASCADE)
    document = models.ForeignKey("KnowledgeBaseDocument", on_delete=models.CASCADE, related_name='document_chunks')
    chunk_document_type = models.CharField(max_length=100, choices=UPLOAD_FILES_SUPPORTED_FORMATS, blank=True, null=True)
    chunk_number = models.IntegerField()
    chunk_content = models.TextField()
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
