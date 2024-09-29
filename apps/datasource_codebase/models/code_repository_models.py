#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: code_repository_models.py
#  Last Modified: 2024-09-26 20:30:21
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:37:14
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

import os

import boto3
from django.db import models
from slugify import slugify

from apps._services.codebase.codebase_decoder import CodeBaseDecoder
from config.settings import MEDIA_URL


class CodeBaseRepository(models.Model):
    knowledge_base = models.ForeignKey("CodeRepositoryStorageConnection", on_delete=models.CASCADE,
                                       related_name="code_base_repositories")
    repository_name = models.CharField(max_length=1000)
    repository_description = models.TextField()
    repository_metadata = models.JSONField()  # auto
    repository_uri = models.CharField(max_length=1000, null=True, blank=True)

    # to associate the element with the Weaviate object
    knowledge_base_uuid = models.CharField(max_length=1000, null=True, blank=True)

    # Documents have chunks
    repository_content_temporary = models.TextField(blank=True, null=True)  # This will be emptied before indexing

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return slugify(self.repository_name) + " - " + self.knowledge_base.name + " - " + self.created_at.strftime(
            "%Y%m%d%H%M%S")

    class Meta:
        verbose_name = "Code Base Repository"
        verbose_name_plural = "Code Base Repositories"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["knowledge_base", "repository_name"]),
            models.Index(fields=["knowledge_base", "created_at"]),
            models.Index(fields=["knowledge_base", "updated_at"]),
        ]

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.document_file_name = slugify(self.repository_name)
        self.document_content_temporary = ""
        self.document_description = ""
        super().save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        # delete the document from Weaviate
        client = CodeBaseDecoder.get(self.knowledge_base)
        if client is not None:
            result = client.delete_weaviate_document(
                class_name=self.knowledge_base.class_name,
                document_uuid=self.knowledge_base_uuid)
            if not result["status"]:
                print(f"[CodeRepositoryStorageConnection.delete] Error deleting Weaviate document: {result['error']}")
            # remove the document from the directory
            document_full_path = self.repository_uri
            boto3_client = boto3.client('s3')
            bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
            s3_path = document_full_path.split(MEDIA_URL)[1]
            s3_path = s3_path.replace('/', '')
            s3_path = f"{s3_path}/"
            if document_full_path is not None:
                try:
                    boto3_client.delete_object(Bucket=bucket_name, Key=s3_path)
                except Exception as e:
                    print(f"[CodeBaseRepository.delete] Error deleting S3 object: {str(e)}")
        # delete the object from ORM
        super().delete(using, keep_parents)
