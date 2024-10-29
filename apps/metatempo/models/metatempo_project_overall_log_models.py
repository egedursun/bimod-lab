#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: metatempo_project_overall_log_models.py
#  Last Modified: 2024-10-28 19:41:41
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-28 19:41:41
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


class MetaTempoProjectOverallLog(models.Model):
    metatempo_connection = models.ForeignKey('metatempo.MetaTempoConnection', on_delete=models.CASCADE)

    #################################################################################################################
    # AI Generated Fields
    overall_activity_summary = models.TextField(null=True, blank=True)
    overall_key_insights = models.JSONField(null=True, blank=True)
    overall_work_intensity = models.IntegerField(null=True, blank=True)
    overall_application_usage_stats = models.JSONField(null=True, blank=True)
    # :-> Mathematical average of individual 'interval logs' in the interval X

    datestamp = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.metatempo_connection} - {self.datestamp}'

    class Meta:
        verbose_name = 'MetaTempo Project Overall Log'
        verbose_name_plural = 'MetaTempo Project Overall Logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['metatempo_connection']),
            models.Index(fields=['datestamp']),
            models.Index(fields=['overall_work_intensity']),
        ]
