#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: ml_model_storage_models.py
#  Last Modified: 2024-10-05 01:39:48
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

import boto3
from django.db import models
from slugify import slugify

from apps.datasource_ml_models.utils import (
    ML_MODEL_ITEM_CATEGORIES
)

from config import settings


class DataSourceMLModelConnection(models.Model):
    assistant = models.ForeignKey(
        'assistants.Assistant',
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=255)
    description = models.TextField()

    model_object_category = models.CharField(
        max_length=20,
        choices=ML_MODEL_ITEM_CATEGORIES
    )

    directory_full_path = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

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
        unique_together = [
            [
                'assistant',
                'name'
            ],
        ]
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=[
                'assistant',
                'name'
            ]),
            models.Index(fields=[
                'assistant',
                'model_object_category'
            ]),
            models.Index(fields=[
                'assistant',
                'directory_full_path'
            ]),
            models.Index(fields=[
                'assistant',
                'created_at'
            ]),
        ]

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ):

        if not self.directory_full_path:
            base_dir = self.assistant.ml_models_base_directory
            dir_suffix = self.model_object_category
            full_path = f"{base_dir}{dir_suffix}/"
            self.directory_full_path = full_path

        super().save(
            force_insert,
            force_update,
            using,
            update_fields
        )

    def delete(self, using=None, keep_parents=False):
        if self.directory_full_path is not None:

            try:
                s3c = boto3.client('s3')
                bucket = settings.AWS_STORAGE_BUCKET_NAME

                s3c.delete_object(
                    Bucket=bucket,
                    Key=self.directory_full_path
                )

            except IOError:
                pass

        super().delete(using, keep_parents)
