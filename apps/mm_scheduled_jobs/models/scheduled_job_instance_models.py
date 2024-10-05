#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: scheduled_job_instance_models.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:43
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: scheduled_job_instance_models.py
#  Last Modified: 2024-09-28 16:44:41
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:02:05
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.db import models

from apps.mm_scheduled_jobs.models import ScheduledJob
from apps.mm_scheduled_jobs.utils import SCHEDULED_JOB_INSTANCE_STATUSES


class ScheduledJobInstance(models.Model):
    """
    ScheduledJobInstance Model:
    - Purpose: Represents an instance of a scheduled job execution, tracking the status, logs, and execution metadata of the job instance.
    - Key Fields:
        - `scheduled_job`: ForeignKey linking to the `ScheduledJob` model that this instance belongs to.
        - `status`: The current status of the job instance (e.g., Pending, Building, Completed).
        - `logs`: A JSON field storing logs related to the job's execution.
        - `execution_index`: An integer field representing the execution index or order.
        - `started_at`, `ended_at`: Timestamps for when the job instance started and ended.
    - Meta:
        - `verbose_name`: "Scheduled Job Instance"
        - `verbose_name_plural`: "Scheduled Job Instances"
        - `ordering`: Orders job instances by start date in descending order.
        - `indexes`: Indexes on various fields, including combinations of `scheduled_job`, `status`, `started_at`, and `ended_at` for optimized queries.
    """

    scheduled_job = models.ForeignKey(ScheduledJob, on_delete=models.CASCADE, related_name='scheduled_job_instances',
                                      null=True)
    status = models.CharField(max_length=255, choices=SCHEDULED_JOB_INSTANCE_STATUSES, default='pending')
    logs = models.JSONField(default=list)
    execution_index = models.IntegerField(default=0, null=True)

    # Metadata
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
