#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: forum_category_models.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:41
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


class ForumCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " - " + self.slug + " - " + self.created_at.strftime("%Y%m%d%H:%M:%S")

    class Meta:
        verbose_name = "Forum Category"
        verbose_name_plural = "Forum Categories"
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=[
                    'name',
                    'slug',
                    'created_at'
                ]
            ),
            models.Index(
                fields=[
                    'name',
                    'slug',
                    'created_at', 'updated_at'
                ]
            ),
        ]
