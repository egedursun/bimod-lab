#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: leanmod_scheduled_job_instance_models.py
#  Last Modified: 2024-12-07 13:56:53
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-07 13:56:53
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

from apps.mm_scheduled_jobs.utils import (
    SCHEDULED_JOB_INSTANCE_STATUSES
)


class LeanModScheduledJobInstance(models.Model):
    scheduled_job = models.ForeignKey(
        'mm_scheduled_jobs.LeanModScheduledJob',
        on_delete=models.CASCADE,
        related_name='scheduled_job_instances',
        null=True
    )

    status = models.CharField(
        max_length=255,
        choices=SCHEDULED_JOB_INSTANCE_STATUSES,
        default='pending'
    )

    logs = models.JSONField(default=list)
    execution_index = models.IntegerField(default=0, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.scheduled_job.name + ' - ' + self.status + ' - ' + self.started_at.strftime(
            '%Y%m%d%H%M%S')

    class Meta:
        ordering = ['-started_at']

        verbose_name = 'LeanMod Scheduled Job Instance'
        verbose_name_plural = 'LeanMod Scheduled Job Instances'

        indexes = [
            models.Index(fields=[
                'scheduled_job',
                'status',
                'started_at'
            ]),
            models.Index(fields=[
                'scheduled_job',
                'status',
                'started_at',
                'ended_at'
            ]),
            models.Index(fields=[
                'scheduled_job',
                'status',
                'started_at',
                'ended_at',
                'id'
            ]),
            models.Index(fields=[
                'scheduled_job',
                'status',
                'started_at',
                'ended_at',
                'id',
                'status'
            ]),
            models.Index(fields=[
                'scheduled_job',
                'status',
                'started_at',
                'ended_at',
                'id',
                'status',
                'logs'
            ]),
        ]
