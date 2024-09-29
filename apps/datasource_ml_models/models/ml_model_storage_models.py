#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: ml_model_storage_models.py
#  Last Modified: 2024-09-27 23:54:09
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:47:52
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

import boto3
from django.db import models
from slugify import slugify

from apps.datasource_ml_models.utils import MODEL_OBJECT_CATEGORIES
from config import settings


class DataSourceMLModelConnection(models.Model):
    """
    DataSourceMLModelConnection Model:
    - Purpose: Represents a connection to an ML model storage system, including configurations for model categories, directory paths, and storage settings.
    - Key Fields:
        - `assistant`: ForeignKey linking to the `Assistant` model.
        - `name`: The name of the ML model storage connection.
        - `description`: A description of the connection.
        - `model_object_category`: The category of the ML model (e.g., PyTorch Model).
        - `directory_full_path`: The full directory path for storing ML model files.
        - `directory_schema`: JSON representation of the directory structure.
        - `interpretation_temperature`, `interpretation_maximum_tokens`: Parameters for interpreting model content.
        - `created_at`, `updated_at`: Timestamps for creation and last update.
    - Methods:
        - `save()`: Overridden to ensure the directory path is set if not provided.
        - `delete()`: Overridden to remove the associated directory and files from AWS S3 storage.
    """

    assistant = models.ForeignKey('assistants.Assistant', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    model_object_category = models.CharField(max_length=20, choices=MODEL_OBJECT_CATEGORIES)

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
        verbose_name = 'Data Source ML Model Connection'
        verbose_name_plural = 'Data Source ML Model Connections'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['assistant', 'name']),
            models.Index(fields=['assistant', 'model_object_category']),
            models.Index(fields=['assistant', 'directory_full_path']),
            models.Index(fields=['assistant', 'created_at']),
        ]

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.directory_full_path:
            base_dir = self.assistant.ml_models_base_directory
            dir_suffix = self.model_object_category
            full_path = f"{base_dir}{dir_suffix}/"
            self.directory_full_path = full_path
        super().save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        if self.directory_full_path is not None:
            try:
                # remove from s3 storage
                boto3_client = boto3.client('s3')
                bucket_name = settings.AWS_STORAGE_BUCKET_NAME
                boto3_client.delete_object(Bucket=bucket_name, Key=self.directory_full_path)
            except IOError:
                pass  # Directory might not exist or might not be empty
        super().delete(using, keep_parents)
