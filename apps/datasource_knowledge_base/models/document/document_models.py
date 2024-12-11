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

import os

import boto3
from django.db import models
from slugify import slugify

from apps.core.vector_operations.vector_document.vector_store_decoder import (
    KnowledgeBaseSystemDecoder
)

from apps.datasource_knowledge_base.utils import (
    UPLOAD_FILES_SUPPORTED_FORMATS
)

from config.settings import MEDIA_URL


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

    document_description = models.TextField()
    document_metadata = models.JSONField()

    document_uri = models.CharField(
        max_length=1000,
        null=True,
        blank=True
    )

    knowledge_base_uuid = models.CharField(
        max_length=1000,
        null=True,
        blank=True
    )

    document_content_temporary = models.TextField(
        blank=True,
        null=True
    )

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

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ):
        self.document_file_name = slugify(self.document_file_name)

        self.document_content_temporary = ""
        self.document_description = ""

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
        c = KnowledgeBaseSystemDecoder.get(
            self.knowledge_base
        )

        if c is not None:
            o = c.delete_weaviate_document(
                class_name=self.knowledge_base.class_name,
                document_uuid=self.knowledge_base_uuid
            )

            if not o["status"]:
                pass

            doc_uri = self.document_uri
            s3c = boto3.client('s3')

            bucket = os.getenv('AWS_STORAGE_BUCKET_NAME')

            bucket_path = doc_uri.split(MEDIA_URL)[1]
            bucket_path = bucket_path.replace('/', '')
            bucket_path = f"{bucket_path}/"

            if doc_uri is not None:
                try:
                    s3c.delete_object(
                        Bucket=bucket,
                        Key=bucket_path
                    )

                except Exception as e:
                    pass

        super().delete(
            using,
            keep_parents
        )
