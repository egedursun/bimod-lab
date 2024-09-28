#  Copyright Policy & Ownership
#
#  Bimod.io is a product of BMD Holdings. All materials, including but not limited to software, code, documentation,
#  graphics, design elements, and user interfaces provided by Bimod.io are protected by copyright law and international
#  treaties.
#  All content within Bimod.io is the exclusive property of BMD Holdings, unless otherwise stated.
#  Unauthorized use, distribution, or reproduction of any material contained in this software without the express
#  written consent of BMD Holdings is strictly prohibited.
#  Users may not copy, modify, distribute, display, perform, or create derivative works of Bimod.io without prior
#  written permission from BMD Holdings.

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
