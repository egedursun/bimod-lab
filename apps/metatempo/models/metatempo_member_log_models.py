#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: metatempo_member_log_models.py
#  Last Modified: 2024-10-28 19:41:02
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-28 19:41:03
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


class MetaTempoMemberLog(models.Model):
    metatempo_connection = models.ForeignKey('metatempo.MetaTempoConnection', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    screenshot_image = models.ImageField(upload_to='metatempo/member_logs/%Y/%m/%d/', null=True, blank=True)

    #################################################################################################################
    # AI Generated Fields
    activity_summary = models.TextField(null=True, blank=True)
    activity_tags = models.JSONField(null=True, blank=True)
    work_intensity = models.IntegerField(null=True, blank=True)  # Score between 0-100
    application_usage_stats = models.JSONField(null=True, blank=True)
    #################################################################################################################

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.metatempo_connection} - {self.timestamp}'

    class Meta:
        verbose_name = 'MetaTempo Member Log'
        verbose_name_plural = 'MetaTempo Member Logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['metatempo_connection', 'user']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['work_intensity']),
        ]
