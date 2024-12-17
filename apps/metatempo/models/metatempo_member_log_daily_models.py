#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: metatempo_member_log_daily_models.py
#  Last Modified: 2024-10-28 19:55:46
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-28 19:55:47
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


class MetaTempoMemberLogDaily(models.Model):
    metatempo_connection = models.ForeignKey(
        'metatempo.MetaTempoConnection',
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    logs = models.ManyToManyField('metatempo.MetaTempoMemberLog', blank=True)

    #################################################################################################################

    daily_activity_summary = models.TextField(null=True, blank=True)
    key_tasks = models.JSONField(null=True, blank=True)

    overall_work_intensity = models.IntegerField(
        null=True,
        blank=True
    )
    application_usage_stats = models.JSONField(null=True, blank=True)

    #################################################################################################################

    datestamp = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.metatempo_connection} - {self.datestamp}'

    class Meta:
        verbose_name = 'MetaTempo Member Log Daily'
        verbose_name_plural = 'MetaTempo Member Log Dailies'

        ordering = ['-created_at']

        indexes = [
            models.Index(fields=[
                'metatempo_connection',
                'user'
            ]),
            models.Index(fields=[
                'datestamp'
            ]),
            models.Index(fields=[
                'overall_work_intensity'
            ]),
        ]
