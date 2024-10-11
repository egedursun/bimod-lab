#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: media_storage_models.py
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

import os

import boto3
from django.db import models
from slugify import slugify

from apps.datasource_media_storages.utils import MEDIA_MANAGER_ITEM_TYPES
from config.settings import MEDIA_URL


class DataSourceMediaStorageConnection(models.Model):
    assistant = models.ForeignKey('assistants.Assistant', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    media_category = models.CharField(max_length=20, choices=MEDIA_MANAGER_ITEM_TYPES)
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
        if self.directory_full_path and os.path.exists(self.directory_full_path):
            s3c = boto3.client('s3')
            bucket = os.getenv('AWS_STORAGE_BUCKET_NAME')
            bucket_path = self.directory_full_path.split(MEDIA_URL)[1]
            bucket_path = bucket_path.replace('/', '')
            bucket_path = f"{bucket_path}/"
            try:
                s3c.delete_object(Bucket=bucket, Key=bucket_path)
            except Exception as e:
                pass
        super().delete(using, keep_parents)
