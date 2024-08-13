"""
Module Overview: This module defines models for managing machine learning (ML) model connections and items within an assistant-based application. It includes configurations for ML model categories, storage paths, and handling the uploading and deletion of ML models in storage systems like AWS S3.

Dependencies:
- `os`, `random`: Python standard libraries for file path manipulation and generating random numbers.
- `boto3`: Used for interacting with AWS S3 to manage ML model storage.
- `paramiko`: Used for SSH-related tasks.
- `django.db.models`: Django's ORM for defining database models.
- `slugify`: Used to generate URL-friendly slugs for file and directory names.
- `config.settings`: Application settings, particularly for accessing storage-related configurations.
- `.tasks.upload_model_to_ml_model_base`: Asynchronous task for uploading ML models to storage.
"""

import random

import boto3
from django.db import models
from slugify import slugify

from config import settings
from .tasks import upload_model_to_ml_model_base


MODEL_OBJECT_CATEGORIES = (
    ('pth', 'PyTorch Model'),
)


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
        return self.name + ' - ' + slugify(self.directory_full_path) + ' - ' + self.created_at.strftime('%Y-%m-%d %H:%M:%S')

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


class DataSourceMLModelItem(models.Model):
    """
    DataSourceMLModelItem Model:
    - Purpose: Represents an individual ML model file within a storage connection, including metadata like file name, size, and storage path.
    - Key Fields:
        - `ml_model_base`: ForeignKey linking to the `DataSourceMLModelConnection` model.
        - `ml_model_name`: The name of the ML model file.
        - `description`: A description of the ML model.
        - `ml_model_size`: The size of the ML model file.
        - `interpretation_temperature`: Parameter for interpreting model content.
        - `full_file_path`: The full path to the ML model file in storage.
        - `file_bytes`: BinaryField for storing the file's content temporarily before uploading.
        - `created_at`, `updated_at`: Timestamps for creation and last update.
    - Methods:
        - `save()`: Overridden to slugify the file name, generate a unique file path, and trigger asynchronous model upload to storage.
    """

    ml_model_base = models.ForeignKey('datasource_ml_models.DataSourceMLModelConnection',
                                     on_delete=models.CASCADE, related_name='items')

    ml_model_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    ml_model_size = models.BigIntegerField(null=True, blank=True)

    interpretation_temperature = models.FloatField(default=0.25)

    full_file_path = models.CharField(max_length=1000, blank=True, null=True)
    file_bytes = models.BinaryField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (self.ml_model_name + ' - ' + slugify(self.full_file_path) + ' - ' +
                self.created_at.strftime('%Y-%m-%d %H:%M:%S'))

    class Meta:
        verbose_name = 'Data Source ML Model Item'
        verbose_name_plural = 'Data Source ML Model Items'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['ml_model_base', 'ml_model_name']),
            models.Index(fields=['ml_model_base', 'description']),
            models.Index(fields=['ml_model_base', 'created_at']),
            models.Index(fields=['ml_model_base', 'updated_at']),
        ]

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.ml_model_name = slugify(self.ml_model_name)
        file_type = MODEL_OBJECT_CATEGORIES[0][0]  # hardcoded for now
        if not self.full_file_path:
            base_dir = self.ml_model_base.directory_full_path
            file_name = self.ml_model_name
            full_path = f"{base_dir}{file_name.split('.')[0]}_{str(random.randint(1_000_000, 9_999_999))}.{file_type}"
            self.full_file_path = full_path
        super().save(force_insert, force_update, using, update_fields)
        # Upload the ml model to ml model base
        upload_model_to_ml_model_base.delay(file_bytes=self.file_bytes, full_path=self.full_file_path)
