#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: academy_course_section_models.py
#  Last Modified: 2024-11-03 17:24:00
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-03 17:24:00
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


class AcademyCourseSection(models.Model):
    course = models.ForeignKey(
        'bmd_academy.AcademyCourse',
        on_delete=models.CASCADE,
        related_name='sections'
    )

    section_name = models.CharField(max_length=1_000)

    section_slug = models.SlugField(
        max_length=1_000,
        null=True,
        blank=True
    )

    section_description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.section_name + ' - ' + self.course.course_title

    class Meta:
        verbose_name = 'Academy Course Section'
        verbose_name_plural = 'Academy Course Sections'

        ordering = ['-created_at']

        indexes = [
            models.Index(
                fields=[
                    'section_name',
                    'created_at'
                ]
            ),
        ]
        unique_together = [
            ['course', 'section_name'],
        ]

    def save(self, *args, **kwargs):
        if not self.section_slug:
            self.section_slug = slugify.slugify(self.course.course_slug + '-' + self.section_name)

        super(AcademyCourseSection, self).save(*args, **kwargs)
