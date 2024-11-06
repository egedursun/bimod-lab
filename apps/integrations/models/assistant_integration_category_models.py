#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: assistant_integration_category_models.py
#  Last Modified: 2024-11-05 19:23:46
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-05 19:23:47
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
from slugify import slugify


class AssistantIntegrationCategory(models.Model):
    category_name = models.CharField(max_length=1000, null=False, blank=False)
    category_description = models.TextField(null=True, blank=True)
    category_image_url = models.URLField(null=True, blank=True)
    tags = models.JSONField(null=True, blank=True)
    category_slug = models.SlugField(max_length=1000, null=True, blank=True, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'Assistant Integration Category'
        verbose_name_plural = 'Assistant Integration Categories'
        unique_together = ['category_name']
        indexes = [
            models.Index(fields=['category_name']),
        ]

    def save(self, *args, **kwargs):
        if not self.category_slug:
            self.category_slug = slugify(self.category_name)
        super(AssistantIntegrationCategory, self).save(*args, **kwargs)
