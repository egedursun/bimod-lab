#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: datasource_website_item_models.py
#  Last Modified: 2024-12-07 19:17:22
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-07 19:17:22
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.db import models

from apps.datasource_website.utils import (
    WebsiteIndexingMethodologyChoicesNames,
    WEBSITE_CRAWLING_METHODOLOGY_CHOICES
)


class DataSourceWebsiteStorageItem(models.Model):
    storage = models.ForeignKey(
        'datasource_website.DataSourceWebsiteStorageConnection',
        on_delete=models.CASCADE,
        related_name='storage_items',
    )

    website_url = models.URLField(
        max_length=10000,
        null=True,
        blank=True,
    )

    crawling_methodology = models.CharField(
        max_length=100,
        choices=WEBSITE_CRAWLING_METHODOLOGY_CHOICES,
        default=WebsiteIndexingMethodologyChoicesNames.TEXT_CONTENT,
    )

    n_chunks_indexed_status = models.IntegerField(default=0)
    n_chunks = models.IntegerField(default=0)

    sitemap_content = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by_user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='created_website_storage_items',
        null=True,
        blank=True,
    )

    class Meta:
        db_table = 'datasource_website_storage_item'
        verbose_name = "Website Storage Item"
        verbose_name_plural = "Website Storage Items"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=[
                'website_url'
            ]),
            models.Index(fields=[
                'crawling_methodology'
            ]),
            models.Index(fields=[
                'created_at'
            ]),
            models.Index(fields=[
                'updated_at'
            ]),
            models.Index(fields=[
                'website_url',
                'crawling_methodology'
            ]),
            models.Index(fields=[
                'website_url',
                'created_at'
            ]),
        ]

    def __str__(self):
        return f"{self.website_url} - {self.storage.name} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
