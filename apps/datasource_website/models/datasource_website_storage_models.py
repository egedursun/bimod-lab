#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: datasource_website_storage_models.py
#  Last Modified: 2024-12-07 19:17:07
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-07 19:17:07
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

from apps.datasource_knowledge_base.utils import EMBEDDING_VECTORIZER_MODELS
from apps.datasource_website.utils import VECTOR_INDEX_PATH_WEBSITE_ITEMS


class DataSourceWebsiteStorageConnection(models.Model):
    assistant = models.ForeignKey(
        'assistants.Assistant',
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=1000)
    description = models.TextField()

    vector_index_path = models.CharField(
        max_length=1000,
        null=True,
        blank=True
    )

    vectorizer = models.CharField(
        max_length=100,
        choices=EMBEDDING_VECTORIZER_MODELS,
        default="text2vec-openai",
        null=True,
        blank=True
    )

    embedding_chunk_size = models.IntegerField(default=1024)
    embedding_chunk_overlap = models.IntegerField(default=256)
    search_instance_retrieval_limit = models.IntegerField(default=10)

    maximum_pages_to_index = models.IntegerField(default=1000)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by_user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='created_website_storage_connections'
    )

    def __str__(self):
        return f"{self.name} - {self.assistant.name} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

    class Meta:
        verbose_name = "Website Storage Connection"
        verbose_name_plural = "Website Storage Connections"
        ordering = ['-created_at']
        unique_together = [
            [
                'assistant',
                'name'
            ]
        ]
        indexes = [
            models.Index(fields=[
                'assistant',
                'name'
            ]),
            models.Index(fields=[
                'assistant',
                'created_at'
            ]),
            models.Index(fields=[
                'assistant',
                'updated_at'
            ])
        ]

    def save(self, *args, **kwargs):
        super(DataSourceWebsiteStorageConnection, self).save(*args, **kwargs)

        if self.vector_index_path is None or self.vector_index_path == "":
            self.vector_index_path = os.path.join(
                VECTOR_INDEX_PATH_WEBSITE_ITEMS,
                f'website_storage_index_{self.id}.index'
            )
            self.save()
