import os
import random

from django.db import models
from slugify import slugify
from .tasks import upload_model_to_ml_model_base


MODEL_OBJECT_CATEGORIES = (
    ('pth', 'PyTorch Model'),
)


class DataSourceMLModelConnection(models.Model):
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

            os.system(f"mkdir -p {full_path}")
            os.system(f"touch {full_path}/__init__.py")
        super().save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        # Remove the directory
        if self.directory_full_path is not None:
            os.system(f"rm -rf {self.directory_full_path}")
        super().delete(using, keep_parents)


class DataSourceMLModelItem(models.Model):
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
