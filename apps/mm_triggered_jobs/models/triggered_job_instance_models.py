#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: triggered_job_instance_models.py
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

from django.db import models

from apps.mm_triggered_jobs.models import (
    TriggeredJob
)

from apps.mm_triggered_jobs.utils import (
    TRIGGERED_JOB_INSTANCE_STATUSES
)


class TriggeredJobInstance(models.Model):
    triggered_job = models.ForeignKey(
        TriggeredJob,
        on_delete=models.CASCADE,
        related_name='triggered_job_instances',
        null=True
    )

    status = models.CharField(
        max_length=255,
        choices=TRIGGERED_JOB_INSTANCE_STATUSES,
        default='pending'
    )

    webhook_payload = models.JSONField(default=dict)
    logs = models.JSONField(default=list)

    execution_index = models.IntegerField(default=0, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.triggered_job.name + ' - ' + self.status + ' - ' + self.started_at.strftime('%Y%m%d%H%M%S')

    class Meta:
        ordering = ['-started_at']

        verbose_name = 'Triggered Job Instance'
        verbose_name_plural = 'Triggered Job Instances'

        indexes = [
            models.Index(fields=[
                'triggered_job',
                'status',
                'started_at'
            ]),
            models.Index(fields=[
                'triggered_job',
                'status',
                'started_at',
                'ended_at'
            ]),
            models.Index(fields=[
                'triggered_job',
                'status',
                'started_at',
                'ended_at',
                'id'
            ]),
            models.Index(fields=[
                'triggered_job',
                'status',
                'started_at',
                'ended_at',
                'id',
                'status'
            ]),
            models.Index(fields=[
                'triggered_job',
                'status',
                'started_at',
                'ended_at',
                'id',
                'status',
                'logs'
            ]),
            models.Index(fields=[
                'triggered_job',
                'status',
                'started_at',
                'ended_at',
                'id',
                'status',
                'logs',
                'webhook_payload'
            ]),
        ]
