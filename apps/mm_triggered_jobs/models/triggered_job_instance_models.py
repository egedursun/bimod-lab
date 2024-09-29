#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: triggered_job_instance_models.py
#  Last Modified: 2024-09-28 19:54:22
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:04:04
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

#
from django.db import models

from apps.mm_triggered_jobs.models import TriggeredJob
from apps.mm_triggered_jobs.utils import TRIGGERED_JOB_INSTANCE_STATUSES


class TriggeredJobInstance(models.Model):
    """
    TriggeredJobInstance Model:
    - Purpose: Represents an instance of a triggered job execution, tracking the status, webhook payload, logs, and execution metadata of the job instance.
    - Key Fields:
        - `triggered_job`: ForeignKey linking to the `TriggeredJob` model that this instance belongs to.
        - `status`: The current status of the job instance (e.g., Pending, Building, Completed).
        - `webhook_payload`: A JSON field storing the payload received from the webhook that triggered the job.
        - `logs`: A JSON field storing logs related to the job's execution.
        - `execution_index`: An integer field representing the execution index or order.
        - `started_at`, `ended_at`: Timestamps for when the job instance started and ended.
    - Meta:
        - `verbose_name`: "Triggered Job Instance"
        - `verbose_name_plural`: "Triggered Job Instances"
        - `ordering`: Orders job instances by start date in descending order.
        - `indexes`: Indexes on various fields, including combinations of `triggered_job`, `status`, `started_at`, `ended_at`, and `logs` for optimized queries.
    """

    triggered_job = models.ForeignKey(TriggeredJob, on_delete=models.CASCADE, related_name='triggered_job_instances',
                                      null=True)
    status = models.CharField(max_length=255, choices=TRIGGERED_JOB_INSTANCE_STATUSES, default='pending')

    webhook_payload = models.JSONField(default=dict)
    logs = models.JSONField(default=list)
    execution_index = models.IntegerField(default=0, null=True)

    # Metadata
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.triggered_job.name + ' - ' + self.status + ' - ' + self.started_at.strftime('%Y%m%d%H%M%S')

    class Meta:
        ordering = ['-started_at']
        verbose_name = 'Triggered Job Instance'
        verbose_name_plural = 'Triggered Job Instances'
        indexes = [
            models.Index(fields=['triggered_job', 'status', 'started_at']),
            models.Index(fields=['triggered_job', 'status', 'started_at', 'ended_at']),
            models.Index(fields=['triggered_job', 'status', 'started_at', 'ended_at', 'id']),
            models.Index(fields=['triggered_job', 'status', 'started_at', 'ended_at', 'id', 'status']),
            models.Index(fields=['triggered_job', 'status', 'started_at', 'ended_at', 'id', 'status', 'logs']),
            models.Index(fields=['triggered_job', 'status', 'started_at', 'ended_at', 'id', 'status', 'logs',
                                 'webhook_payload']),
        ]
