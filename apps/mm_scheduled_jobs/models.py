"""
Module Overview: This module defines models related to scheduled jobs and their instances within an assistant-based application. It includes functionality for setting up periodic tasks, tracking job statuses, and logging the execution of scheduled jobs.

Dependencies:
- `django.db.models`: Django's ORM for defining database models.
- `django_celery_beat.models.PeriodicTask`: Used for scheduling tasks in a Django/Celery environment.
"""

from django.db import models
from django_celery_beat.models import PeriodicTask


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
    scheduled_job_instances = models.ManyToManyField('ScheduledJobInstance', related_name='scheduled_jobs')

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
        return self.name + ' - ' + self.assistant.name + ' - ' + self.created_by_user.username + ' - ' + self.created_at.strftime('%Y%m%d%H%M%S')

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


SCHEDULED_JOB_INSTANCE_STATUSES = [
    ('pending', 'Pending'),
    ('building', 'Building'),
    ('initializing_assistant', 'Initializing Assistant'),
    ('generating', 'Generating'),
    ('saving_logs', 'Saving Logs'),
    ('cleaning_up', 'Cleaning Up'),
    ('completed', 'Completed'),
    ('failed', 'Failed'),
]


class ScheduledJobInstanceStatusesNames:
    PENDING = 'pending'
    BUILDING = 'building'
    INITIALIZING_ASSISTANT = 'initializing_assistant'
    GENERATING = 'generating'
    SAVING_LOGS = 'saving_logs'
    CLEANING_UP = 'cleaning_up'
    COMPLETED = 'completed'
    FAILED = 'failed'


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

    scheduled_job = models.ForeignKey(ScheduledJob, on_delete=models.CASCADE, related_name='instances', null=True)
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
