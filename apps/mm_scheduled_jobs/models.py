from django.db import models
from django_celery_beat.models import PeriodicTask

from apps.mm_scheduled_jobs.tasks import add_periodic_task

# Create your models here.


class ScheduledJob(models.Model):
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
    scheduled_job = models.ForeignKey(ScheduledJob, on_delete=models.CASCADE, related_name='instances', null=True)
    status = models.CharField(max_length=255, choices=SCHEDULED_JOB_INSTANCE_STATUSES, default='pending')
    logs = models.JSONField(default=list)

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
