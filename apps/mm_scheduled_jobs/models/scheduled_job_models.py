#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: scheduled_job_models.py
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
#  File: scheduled_job_models.py
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


class ScheduledJob(models.Model):
    """
    ScheduledJob Model:
    - Purpose: Represents a scheduled job configured to run at specific intervals (using cron-like fields). It stores details about the job, including its name, description, scheduling details, and metadata about its creation.
    - Key Fields:
        - `name`: The name of the scheduled job.
        - `task_description`: A description of the task that the job will execute.
        - `step_guide`: A JSON field storing the steps or guide for the job.
        - `assistant`: ForeignKey linking to the `Assistant` model associated with the job.
        - `scheduled_job_instances`: ManyToManyField linking to `ScheduledJobInstance` models representing the job's executions.
        - `minute`, `hour`, `day_of_week`, `day_of_month`, `month_of_year`: Fields for specifying the cron-like scheduling parameters.
        - `current_run_count`: Tracks the number of times the job has run.
        - `maximum_runs`: The maximum number of times the job is allowed to run.
        - `created_at`, `updated_at`: Timestamps for creation and last update.
        - `created_by_user`: ForeignKey linking to the `User` who created the job.
    - Meta:
        - `verbose_name`: "Scheduled Job"
        - `verbose_name_plural`: "Scheduled Jobs"
        - `ordering`: Orders jobs by creation date in descending order.
        - `indexes`: Indexes on various fields, including combinations of `name`, `assistant`, `created_by_user`, and `created_at` for optimized queries.
    """

    name = models.CharField(max_length=255)
    task_description = models.TextField(blank=True, null=True)
    step_guide = models.JSONField(default=list)

    assistant = models.ForeignKey('assistants.Assistant', on_delete=models.CASCADE, related_name='scheduled_jobs')

    # TYPE: Cron fields
    minute = models.CharField(max_length=600, blank=True, null=True)
    hour = models.CharField(max_length=240, blank=True, null=True)
    day_of_week = models.CharField(max_length=90, blank=True, null=True)  # e.g., "0,1,2,3,4"
    day_of_month = models.CharField(max_length=310, blank=True, null=True)  # e.g., "1,15,30"
    month_of_year = models.CharField(max_length=120, blank=True, null=True)  # e.g., "1,6,12"

    current_run_count = models.PositiveIntegerField(default=0)
    maximum_runs = models.PositiveIntegerField(default=1000)

    # Metadata
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
