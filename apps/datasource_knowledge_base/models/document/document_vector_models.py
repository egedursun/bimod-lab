#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#
import os

from django.db import models

from apps.datasource_knowledge_base.utils import (
    UPLOAD_FILES_SUPPORTED_FORMATS,
    VECTOR_INDEX_PATH_KNOWLEDGE_BASE_DOCUMENTS
)


class DocumentChunkVectorData(models.Model):
    knowledge_base_document = models.ForeignKey(
        "KnowledgeBaseDocument",
        on_delete=models.CASCADE,
        related_name='document_chunks'
    )

    chunk_document_type = models.CharField(
        max_length=100,
        choices=UPLOAD_FILES_SUPPORTED_FORMATS,
        blank=True,
        null=True
    )

    raw_data = models.JSONField(blank=True, null=True)

    raw_data_hash = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    vector_data = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.knowledge_base_document.document_file_name} - {self.knowledge_base_document.knowledge_base.name}"

    class Meta:
        verbose_name = "Knowledge Base Document Chunk"
        verbose_name_plural = "Knowledge Base Document Chunks"

        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=[
                "knowledge_base_document",
            ]),
            models.Index(fields=[
                "knowledge_base_document",
                "created_at"
            ]),
        ]

    def _get_index_path(self):
        storage_id = self.knowledge_base_document.knowledge_base.id

        return os.path.join(
            VECTOR_INDEX_PATH_KNOWLEDGE_BASE_DOCUMENTS,
            f'knowledge_base_storage_index_{storage_id}.index'
        )
