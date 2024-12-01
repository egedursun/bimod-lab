#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: academy_course_models.py
#  Last Modified: 2024-11-03 17:21:07
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-03 17:21:08
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import slugify
from django.db import models


class AcademyCourse(models.Model):
    course_title = models.CharField(max_length=1_000, unique=True)

    course_slug = models.SlugField(
        max_length=1_000,
        unique=True,
        null=True,
        blank=True
    )

    course_description = models.TextField()
    course_language = models.CharField(max_length=1_000)

    course_instructor = models.ForeignKey(
        'bmd_academy.AcademyCourseInstructor',
        on_delete=models.CASCADE
    )

    course_thumbnail_image_url = models.URLField(null=True, blank=True)
    course_under_construction = models.BooleanField(default=True)

    tags = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.course_title + ' - ' + self.course_language + ' - ' + self.course_instructor.full_name

    class Meta:
        verbose_name = 'Academy Course'
        verbose_name_plural = 'Academy Courses'
        ordering = ['-created_at']
        indexes = [
            models.Index(
                fields=[
                    'course_title',
                    'course_language',
                    'created_at'
                ]
            ),
        ]

    def save(self, *args, **kwargs):
        if not self.course_slug:
            self.course_slug = slugify.slugify(self.course_title)

        super(AcademyCourse, self).save(*args, **kwargs)
