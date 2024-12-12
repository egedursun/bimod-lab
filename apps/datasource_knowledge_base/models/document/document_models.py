#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: document_models.py
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

from django.db import models
from slugify import slugify

from apps.datasource_knowledge_base.utils import (
    UPLOAD_FILES_SUPPORTED_FORMATS
)


class KnowledgeBaseDocument(models.Model):
    knowledge_base = models.ForeignKey(
        "DocumentKnowledgeBaseConnection",
        on_delete=models.CASCADE,
        related_name='knowledge_base_documents'
    )

    document_type = models.CharField(
        max_length=100,
        choices=UPLOAD_FILES_SUPPORTED_FORMATS
    )

    document_file_name = models.CharField(max_length=1000)

    document_uri = models.CharField(
        max_length=1000,
        null=True,
        blank=True
    )

    n_chunks_indexed_status = models.IntegerField(default=0)
    n_chunks = models.IntegerField(default=0)

    document_description = models.TextField(blank=True, null=True)
    document_metadata = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by_user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='created_knowledge_base_documents',
        null=True,
        blank=True,
    )

    def __str__(self):
        return slugify(self.document_file_name) + " - " + self.knowledge_base.name + " - " + str(
            self.knowledge_base.id)

    class Meta:
        verbose_name = "Knowledge Base Document"
        verbose_name_plural = "Knowledge Base Documents"

        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=[
                "knowledge_base",
                "document_file_name"
            ]),
            models.Index(fields=[
                "knowledge_base",
                "created_at"
            ]),
            models.Index(fields=[
                "knowledge_base",
                "updated_at"
            ]),
        ]
