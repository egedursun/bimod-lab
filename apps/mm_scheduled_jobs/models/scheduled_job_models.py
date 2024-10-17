#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: scheduled_job_models.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:45
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
#
#
#

from django.db import models


class ScheduledJob(models.Model):
    name = models.CharField(max_length=255)
    task_description = models.TextField(blank=True, null=True)
    step_guide = models.JSONField(default=list)
    assistant = models.ForeignKey('assistants.Assistant', on_delete=models.CASCADE, related_name='scheduled_jobs')
    minute = models.CharField(max_length=600, blank=True, null=True)
    hour = models.CharField(max_length=240, blank=True, null=True)
    day_of_week = models.CharField(max_length=90, blank=True, null=True)  # e.g., "0,1,2,3,4"
    day_of_month = models.CharField(max_length=310, blank=True, null=True)  # e.g., "1,15,30"
    month_of_year = models.CharField(max_length=120, blank=True, null=True)  # e.g., "1,6,12"
    current_run_count = models.PositiveIntegerField(default=0)
    maximum_runs = models.PositiveIntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='scheduled_jobs')

    def __str__(self):
        return self.name + ' - ' + self.assistant.name + ' - ' + self.created_by_user.username + ' - ' + self.created_at.strftime(
            '%Y%m%d%H%M%S')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Scheduled Job'
        verbose_name_plural = 'Scheduled Jobs'
        indexes = [
            models.Index(fields=['name', 'assistant', 'created_by_user', 'created_at']),
            models.Index(fields=['created_at']),
            models.Index(fields=['assistant']),
            models.Index(fields=['created_by_user']),
            models.Index(fields=['assistant', 'created_by_user']),
            models.Index(fields=['assistant', 'created_by_user', 'created_at']),
            models.Index(fields=['assistant', 'created_by_user', 'created_at', 'name']),
            models.Index(fields=['assistant', 'created_by_user', 'created_at', 'name', 'current_run_count']),
        ]
