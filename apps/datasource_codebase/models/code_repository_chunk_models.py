#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: code_repository_chunk_models.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:46
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


class CodeBaseRepositoryChunk(models.Model):
    knowledge_base = models.ForeignKey(
        "CodeRepositoryStorageConnection",
        on_delete=models.CASCADE
    )

    repository = models.ForeignKey(
        "CodeBaseRepository",
        on_delete=models.CASCADE,
        related_name="repository_chunks"
    )

    chunk_number = models.IntegerField()
    chunk_content = models.TextField()
    chunk_metadata = models.TextField()

    chunk_repository_uri = models.CharField(
        max_length=1000,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    knowledge_base_uuid = models.CharField(
        max_length=1000,
        null=True,
        blank=True
    )

    repository_uuid = models.CharField(
        max_length=1000,
        null=True,
        blank=True
    )

    def __str__(self):
        return str(
            self.chunk_number) + " - " + self.repository.repository_name + " - " + self.knowledge_base.name + " - " + self.created_at.strftime(
            "%Y%m%d%H%M%S")

    class Meta:
        verbose_name = "Code Base Document Chunk"
        verbose_name_plural = "Code Base Document Chunks"

        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=[
                "knowledge_base",
                "repository",
                "chunk_number"
            ]),
            models.Index(fields=[
                "knowledge_base",
                "repository",
                "created_at"
            ]),
            models.Index(fields=[
                "knowledge_base",
                "repository",
                "updated_at"
            ]),
        ]

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ):
        super().save(
            force_insert,
            force_update,
            using,
            update_fields
        )
