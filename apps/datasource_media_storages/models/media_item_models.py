#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: media_item_models.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:48
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
import random

from django.db import models
from slugify import slugify

from apps.datasource_media_storages.tasks import upload_file_to_storage
from apps.datasource_media_storages.utils import MEDIA_FILE_TYPES
from config.settings import MEDIA_URL

logger = logging.getLogger(__name__)


class DataSourceMediaStorageItem(models.Model):
    storage_base = models.ForeignKey(
        'datasource_media_storages.DataSourceMediaStorageConnection',
        on_delete=models.CASCADE,
        related_name='items'
    )

    media_file_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    media_file_size = models.BigIntegerField(null=True, blank=True)

    media_file_type = models.CharField(
        max_length=10,
        choices=MEDIA_FILE_TYPES
    )

    full_file_path = models.CharField(
        max_length=1000,
        blank=True,
        null=True
    )

    file_bytes = models.BinaryField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.media_file_name + ' - ' + self.media_file_type + ' - ' + self.created_at.strftime(
            '%Y-%m-%d %H:%M:%S')

    class Meta:
        verbose_name = 'Data Source Media Storage Item'
        verbose_name_plural = 'Data Source Media Storage Items'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=[
                'storage_base',
                'media_file_name'
            ]),
            models.Index(fields=[
                'storage_base',
                'media_file_type'
            ]),
            models.Index(fields=[
                'storage_base',
                'media_file_size'
            ]),
            models.Index(fields=[
                'storage_base',
                'full_file_path'
            ]),
            models.Index(fields=[
                'storage_base',
                'description'
            ]),
            models.Index(fields=[
                'storage_base',
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

        self.media_file_name = slugify(self.media_file_name)
        file_type = self.media_file_type

        if file_type not in [ft[0] for ft in MEDIA_FILE_TYPES]:
            logger.error(f"Unsupported file type: {file_type}")
            return False

        if not self.full_file_path:
            base_dir = self.storage_base.directory_full_path
            file_name = self.media_file_name

            unique_suffix = str(random.randint(1_000_000, 9_999_999))
            relative_path = f"{base_dir.split(MEDIA_URL)[1]}/{file_name.split('.')[0]}_{unique_suffix}.{file_type}"

            self.full_file_path = f"{MEDIA_URL}{relative_path}"

            upload_file_to_storage.delay(
                file_bytes=self.file_bytes,
                full_path=relative_path,
                media_category=self.storage_base.media_category
            )

        self.file_bytes = None

        super().save(
            force_insert,
            force_update,
            using,
            update_fields
        )
