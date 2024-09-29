#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: media_storage_models.py
#  Last Modified: 2024-09-27 12:19:22
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:46:15
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

from apps.datasource_media_storages.utils import MEDIA_CATEGORIES
from config.settings import MEDIA_URL


class DataSourceMediaStorageConnection(models.Model):
    """
    DataSourceMediaStorageConnection Model:
    - Purpose: Represents a connection to a media storage system, including configurations for media categories, directory paths, and storage settings.
    - Key Fields:
        - `assistant`: ForeignKey linking to the `Assistant` model.
        - `name`: The name of the media storage connection.
        - `description`: A description of the connection.
        - `media_category`: The category of media (e.g., Image, Audio).
        - `directory_full_path`: The full directory path for storing media files.
        - `directory_schema`: JSON representation of the directory structure.
        - `interpretation_temperature`, `interpretation_maximum_tokens`: Parameters for interpreting media content.
        - `created_at`, `updated_at`: Timestamps for creation and last update.
    - Methods:
        - `save()`: Overridden to ensure the directory path is set if not provided.
        - `delete()`: Overridden to remove the associated directory from storage, with support for AWS S3.
    """

    assistant = models.ForeignKey('assistants.Assistant', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    media_category = models.CharField(max_length=20, choices=MEDIA_CATEGORIES)

    directory_full_path = models.CharField(max_length=255, blank=True, null=True)
    directory_schema = models.TextField(blank=True, null=True)

    interpretation_temperature = models.FloatField(default=0.25)
    interpretation_maximum_tokens = models.IntegerField(default=2048)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + ' - ' + slugify(self.directory_full_path) + ' - ' + self.created_at.strftime(
            '%Y-%m-%d %H:%M:%S')

    class Meta:
        verbose_name = 'Data Source Media Storage Connection'
        verbose_name_plural = 'Data Source Media Storage Connections'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['assistant', 'name']),
            models.Index(fields=['assistant', 'media_category']),
            models.Index(fields=['assistant', 'directory_full_path']),
            models.Index(fields=['assistant', 'created_at']),
        ]

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.directory_full_path:
            base_dir = self.assistant.storages_base_directory
            dir_suffix = self.media_category
            full_path = os.path.join(base_dir, dir_suffix)
            self.directory_full_path = full_path
        super().save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        # Remove the directory
        if self.directory_full_path and os.path.exists(self.directory_full_path):
            boto3_client = boto3.client('s3')
            bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
            s3_path = self.directory_full_path.split(MEDIA_URL)[1]
            s3_path = s3_path.replace('/', '')
            s3_path = f"{s3_path}/"
            try:
                boto3_client.delete_object(Bucket=bucket_name, Key=s3_path)
            except Exception as e:
                print(
                    f"[DataSourceMediaStorageConnection.delete] Error occurred while deleting the directory: {str(e)}")
        super().delete(using, keep_parents)
