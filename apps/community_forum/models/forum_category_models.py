#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: forum_category_models.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:39
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: forum_category_models.py
#  Last Modified: 2024-09-26 19:10:04
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:21:29
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.db import models


class ForumCategory(models.Model):
    """
    Represents a category within the forum. Categories are used to group threads
    together based on a common theme or subject.

    Attributes:
        id (AutoField): The primary key for the category.
        name (CharField): The name of the category.
        description (TextField): A detailed description of the category.
        slug (SlugField): A URL-friendly slug for the category.
        created_at (DateTimeField): The date and time when the category was created.
        updated_at (DateTimeField): The date and time when the category was last updated.
    """

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
            models.Index(fields=['name', 'slug', 'created_at']),
            models.Index(fields=['name', 'slug', 'created_at', 'updated_at']),
        ]
