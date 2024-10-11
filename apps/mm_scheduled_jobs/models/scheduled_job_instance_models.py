#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: scheduled_job_instance_models.py
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.db import models

from apps.mm_scheduled_jobs.models import ScheduledJob
from apps.mm_scheduled_jobs.utils import SCHEDULED_JOB_INSTANCE_STATUSES


class ScheduledJobInstance(models.Model):
    scheduled_job = models.ForeignKey(ScheduledJob, on_delete=models.CASCADE, related_name='scheduled_job_instances',
                                      null=True)
    status = models.CharField(max_length=255, choices=SCHEDULED_JOB_INSTANCE_STATUSES, default='pending')
    logs = models.JSONField(default=list)
    execution_index = models.IntegerField(default=0, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.scheduled_job.name + ' - ' + self.status + ' - ' + self.started_at.strftime('%Y%m%d%H%M%S')

    class Meta:
        ordering = ['-started_at']
        verbose_name = 'Scheduled Job Instance'
        verbose_name_plural = 'Scheduled Job Instances'
        indexes = [
            models.Index(fields=['scheduled_job', 'status', 'started_at']),
            models.Index(fields=['scheduled_job', 'status', 'started_at', 'ended_at']),
            models.Index(fields=['scheduled_job', 'status', 'started_at', 'ended_at', 'id']),
            models.Index(fields=['scheduled_job', 'status', 'started_at', 'ended_at', 'id', 'status']),
            models.Index(fields=['scheduled_job', 'status', 'started_at', 'ended_at', 'id', 'status', 'logs']),
        ]
