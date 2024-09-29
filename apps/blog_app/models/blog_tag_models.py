#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: blog_tag_models.py
#  Last Modified: 2024-09-26 18:30:38
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:19:50
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.db import models
from slugify import slugify


class BlogTag(models.Model):
    """
    Represents a tag associated with blog posts.

    Attributes:
        name (str): The name of the tag.
        slug (str): The URL-friendly version of the tag name.
        created_at (datetime): The timestamp when the tag was created.
        updated_at (datetime): The timestamp when the tag was last updated.
    """
    blog_posts = models.ManyToManyField('BlogPost', related_name='tags', blank=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Blog Tag'
        verbose_name_plural = 'Blog Tags'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['slug']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]
