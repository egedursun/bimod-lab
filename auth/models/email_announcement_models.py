#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: email_announcement_models.py
#  Last Modified: 2024-10-23 18:07:25
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-23 18:07:26
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


class BimodEmailAnnouncement(models.Model):
    email_subject_raw = models.CharField(max_length=255)
    title_raw = models.CharField(max_length=255)
    body_raw = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email_subject_raw + ' - ' + self.title_raw + ' - ' + self.created_at.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        verbose_name = 'Bimod Email Announcement'
        verbose_name_plural = 'Bimod Email Announcements'

        ordering = ['-created_at']

        indexes = [
            models.Index(fields=[
                'created_at'
            ]),
            models.Index(fields=[
                'title_raw'
            ]),
            models.Index(fields=[
                'email_subject_raw'
            ]),
        ]
