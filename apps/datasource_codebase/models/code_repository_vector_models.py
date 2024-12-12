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

import os

from django.db import models

from apps.datasource_codebase.utils import (
    VECTOR_INDEX_PATH_CODEBASE_REPOSITORIES
)


class CodeBaseRepositoryChunk(models.Model):
    repository_item = models.ForeignKey(
        "datasource_codebase.CodeBaseRepository",
        on_delete=models.CASCADE,
        null=True,
        blank=True
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
        return f"{self.repository_item.repository_name} - {self.repository_item.knowledge_base.name} - ID: {self.id}"

    class Meta:
        verbose_name = "Code Base Document Chunk"
        verbose_name_plural = "Code Base Document Chunks"

        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=[
                "repository_item",
            ]),
            models.Index(fields=[
                "repository_item",
                "created_at"
            ]),
            models.Index(fields=[
                "repository_item",
                "updated_at"
            ]),
        ]

    def _get_index_path(self):
        storage_id = self.repository_item.knowledge_base.id

        return os.path.join(
            VECTOR_INDEX_PATH_CODEBASE_REPOSITORIES,
            f'codebase_storage_index_{storage_id}.index'
        )
