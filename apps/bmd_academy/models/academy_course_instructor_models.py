#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: academy_course_instructor_models.py
#  Last Modified: 2024-11-03 17:26:16
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-03 17:26:17
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


class AcademyCourseInstructor(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=1_000)
    course_instructor_bio = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name + ' - ' + self.user.email

    class Meta:
        verbose_name = 'Academy Course Instructor'
        verbose_name_plural = 'Academy Course Instructors'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['full_name', 'created_at']),
        ]
