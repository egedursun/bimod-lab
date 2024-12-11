#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: knowledge_base_models.py
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

import logging

from django.db import models

from apps.core.vector_operations.vector_document.vector_store_decoder import (
    KnowledgeBaseSystemDecoder
)

from apps.datasource_knowledge_base.utils import (
    VECTORSTORE_SYSTEMS,
    EMBEDDING_VECTORIZER_MODELS,
    build_weaviate_class_name
)

logger = logging.getLogger(__name__)


class DocumentKnowledgeBaseConnection(models.Model):
    provider = models.CharField(
        max_length=100,
        choices=VECTORSTORE_SYSTEMS
    )

    host_url = models.CharField(max_length=1000)

    provider_api_key = models.CharField(
        max_length=1000,
        null=True,
        blank=True
    )

    assistant = models.ForeignKey(
        'assistants.Assistant',
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=1000)

    class_name = models.CharField(
        max_length=1000,
        null=True,
        blank=True
    )

    description = models.TextField()

    vectorizer = models.CharField(
        max_length=100,
        choices=EMBEDDING_VECTORIZER_MODELS,
        default="text2vec-openai",
        null=True,
        blank=True
    )

    vectorizer_api_key = models.CharField(
        max_length=1000,
        null=True,
        blank=True
    )

    embedding_chunk_size = models.IntegerField(default=1024)
    embedding_chunk_overlap = models.IntegerField(default=256)

    schema_json = models.TextField(null=True, blank=True)
    search_instance_retrieval_limit = models.IntegerField(default=10)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " - " + self.assistant.name + " - " + self.created_at.strftime("%Y%m%d%H%M%S")

    class Meta:
        verbose_name = "Document Knowledge Base Connection"
        verbose_name_plural = "Document Knowledge Base Connections"
        ordering = ["-created_at"]

        unique_together = [
            [
                'host_url',
                'assistant'
            ],
        ]

        indexes = [
            models.Index(
                fields=[
                    "provider",
                    "assistant",
                    "name"
                ]
            ),
            models.Index(
                fields=[
                    "provider",
                    "assistant",
                    "created_at"
                ]
            ),
            models.Index(
                fields=[
                    "provider",
                    "assistant",
                    "updated_at"
                ]
            ),
            models.Index(
                fields=[
                    "class_name"
                ]
            ),
            models.Index(
                fields=[
                    "vectorizer"
                ]
            ),
        ]

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ):

        if self.vectorizer is None:
            self.vectorizer = "text2vec-openai"

        if self.class_name is None:
            self.class_name = build_weaviate_class_name(self)

        try:
            c = KnowledgeBaseSystemDecoder.get(self)

            if c is not None:
                o = c.create_weaviate_classes()
                if not o["status"]:
                    pass

            self.schema_json = c.retrieve_schema()

        except Exception as e:
            logger.error(f"[DocumentKnowledgeBaseConnection] Error creating Weaviate class: {e}")

        super().save(
            force_insert,
            force_update,
            using,
            update_fields
        )

    def delete(
        self,
        using=None,
        keep_parents=False
    ):

        try:
            c = KnowledgeBaseSystemDecoder.get(self)

            if c is not None:

                o = c.delete_weaviate_classes(
                    class_name=self.class_name
                )

                if not o["status"]:
                    pass

        except Exception as e:
            logger.error(f"[DocumentKnowledgeBaseConnection] Error deleting Weaviate class: {e}")

        super().delete(using, keep_parents)
