#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: blog_seo_meta_models.py
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


class BlogSEOMeta(models.Model):
    post = models.OneToOneField(
        "BlogPost",
        on_delete=models.CASCADE,
        related_name='seo_meta'
    )

    meta_title = models.CharField(max_length=300, blank=True)
    meta_description = models.CharField(max_length=1000, blank=True)
    meta_keywords = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return f'SEO Meta for {self.post.title}'

    class Meta:
        verbose_name = 'Blog SEO Meta'
        verbose_name_plural = 'Blog SEO Meta'

        ordering = ['post']

        indexes = [
            models.Index(fields=[
                'post'
            ]),
            models.Index(fields=[
                'meta_title'
            ]),
            models.Index(fields=[
                'meta_description'
            ]),
            models.Index(fields=[
                'meta_keywords'
            ]),
            models.Index(fields=[
                'post',
                'meta_title'
            ]),
            models.Index(fields=[
                'post',
                'meta_description'
            ]),
            models.Index(fields=[
                'post',
                'meta_keywords'
            ]),
        ]
