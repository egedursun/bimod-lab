#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: datasource_website_item_vector_models.py
#  Last Modified: 2024-12-07 19:17:33
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-07 19:17:34
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import os

from django.db import models

from apps.datasource_website.utils import VECTOR_INDEX_PATH_WEBSITE_ITEMS


class WebsiteItemChunkVectorData(models.Model):
    website_item = models.ForeignKey(
        'datasource_website.DataSourceWebsiteStorageItem',
        on_delete=models.CASCADE
    )

    raw_data = models.JSONField(blank=True, null=True)

    raw_data_hash = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    vector_data = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.website_item.storage.name + " - " + self.website_item.storage.assistant.name + " - " + self.website_item.website_url

    class Meta:
        verbose_name = "Website Item Chunk Vector Data"
        verbose_name_plural = "Website Item Chunk Vector Data"
        indexes = [
            models.Index(fields=[
                'website_item'
            ]),
            models.Index(fields=[
                'created_at'
            ]),
            models.Index(fields=[
                'updated_at'
            ]),
        ]

    def _get_index_path(self):
        storage_id = self.website_item.storage.id
        return os.path.join(
            VECTOR_INDEX_PATH_WEBSITE_ITEMS,
            f'website_storage_index_{storage_id}.index'
        )
