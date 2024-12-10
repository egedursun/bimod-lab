#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: blog_post_models.py
#  Last Modified: 2024-10-05 12:51:58
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:34
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
from django.utils import timezone
from slugify import slugify

from apps.blog_app.utils import STATUS_CHOICES


class BlogPost(models.Model):
    title = models.CharField(max_length=255)

    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True
    )

    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    content = models.TextField()

    thumbnail_image = models.ImageField(
        upload_to='blog_post_images/%Y/%m/%d/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(default=timezone.now)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title + ' by ' + self.author.username if self.author else 'admin'

    class Meta:
        ordering = ['-published_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

        indexes = [
            models.Index(
                fields=[
                    'title',
                    'slug'
                ]
            ),

            models.Index(
                fields=[
                    'title',
                    'status'
                ]
            ),

            models.Index(
                fields=[
                    'title',
                    'status',
                    'published_at'
                ]
            ),

            models.Index(
                fields=[
                    'title',
                    'status',
                    'created_at'
                ]
            ),

            models.Index(
                fields=[
                    'title',
                    'status',
                    'updated_at'
                ]
            ),

            models.Index(
                fields=[
                    'title',
                    'status',
                    'published_at',
                    'created_at'
                ]
            ),

            models.Index(
                fields=[
                    'title',
                    'status',
                    'published_at',
                    'updated_at'
                ]
            ),

            models.Index(
                fields=[
                    'title',
                    'status',
                    'created_at',
                    'updated_at'
                ]
            ),

            models.Index(
                fields=[
                    'title',
                    'status',
                    'created_at',
                    'published_at'
                ]
            ),

            models.Index(
                fields=[
                    'title',
                    'status',
                    'updated_at',
                    'published_at'
                ]
            ),
        ]
