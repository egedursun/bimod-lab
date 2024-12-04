#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: ml_model_item_models.py
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

import random

from django.db import models
from slugify import slugify

from apps.datasource_ml_models.tasks import (
    upload_model_to_ml_model_base
)

from apps.datasource_ml_models.utils import (
    ML_MODEL_ITEM_CATEGORIES
)


class DataSourceMLModelItem(models.Model):
    ml_model_base = models.ForeignKey(
        'datasource_ml_models.DataSourceMLModelConnection',
        on_delete=models.CASCADE,
        related_name='items'
    )

    ml_model_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    ml_model_size = models.BigIntegerField(null=True, blank=True)
    interpretation_temperature = models.FloatField(default=0.25)

    full_file_path = models.CharField(
        max_length=1000,
        blank=True,
        null=True
    )

    file_bytes = models.BinaryField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (self.ml_model_name + ' - ' + slugify(self.full_file_path) + ' - ' +
                self.created_at.strftime('%Y-%m-%d %H:%M:%S'))

    class Meta:
        verbose_name = 'Data Source ML Model Item'
        verbose_name_plural = 'Data Source ML Model Items'

        unique_together = [
            [
                'ml_model_base',
                'ml_model_name'
            ],
        ]

        ordering = ['-created_at']

        indexes = [
            models.Index(fields=[
                'ml_model_base',
                'ml_model_name'
            ]),
            models.Index(fields=[
                'ml_model_base',
                'description'
            ]),
            models.Index(fields=[
                'ml_model_base',
                'created_at'
            ]),
            models.Index(fields=[
                'ml_model_base',
                'updated_at'
            ]),
        ]

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ):
        self.ml_model_name = slugify(self.ml_model_name)
        file_type = ML_MODEL_ITEM_CATEGORIES[0][0]

        if not self.full_file_path:
            base_dir = self.ml_model_base.directory_full_path
            f_name = self.ml_model_name
            f_uri = f"{base_dir}{f_name.split('.')[0]}_{str(random.randint(1_000_000, 9_999_999))}.{file_type}"
            self.full_file_path = f_uri

        super().save(
            force_insert,
            force_update,
            using,
            update_fields
        )

        upload_model_to_ml_model_base.delay(
            file_bytes=self.file_bytes,
            full_path=self.full_file_path
        )
