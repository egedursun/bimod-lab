import random

from django.db import models
from slugify import slugify

from apps.datasource_ml_models.tasks import upload_model_to_ml_model_base
from apps.datasource_ml_models.utils import MODEL_OBJECT_CATEGORIES


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
