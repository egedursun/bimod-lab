#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: academy_course_video_models.py
#  Last Modified: 2024-11-03 17:24:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-03 17:24:09
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
import slugify


class AcademyCourseVideo(models.Model):
    course_section = models.ForeignKey('bmd_academy.AcademyCourseSection', on_delete=models.CASCADE, related_name='videos')
    video_title = models.CharField(max_length=1_000)
    video_slug = models.SlugField(max_length=1_000, unique=True, null=True, blank=True)
    video_description = models.TextField(null=True, blank=True)
    video_content_url = models.URLField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.video_title + ' - ' + self.course_section.section_name + ' - ' + self.course_section.course.course_title

    class Meta:
        verbose_name = 'Academy Course Video'
        verbose_name_plural = 'Academy Course Videos'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['video_title', 'created_at']),
        ]
        unique_together = ['course_section', 'video_title']

    def save(self, *args, **kwargs):
        if not self.video_slug:
            self.video_slug = self.course_section.section_slug + '-' + slugify.slugify(self.video_title)
        super(AcademyCourseVideo, self).save(*args, **kwargs)
