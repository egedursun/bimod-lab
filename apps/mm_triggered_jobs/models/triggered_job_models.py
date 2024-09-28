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

from config.settings import BASE_URL


class TriggeredJob(models.Model):
    """
    TriggeredJob Model:
    - Purpose: Represents a job that is triggered by an external event, such as a webhook. It stores details about the job, including its name, description, trigger source, and metadata about its creation.
    - Key Fields:
        - `name`: The name of the triggered job.
        - `task_description`: A description of the task that the job will execute.
        - `step_guide`: A JSON field storing the steps or guide for the job.
        - `trigger_assistant`: ForeignKey linking to the `Assistant` model associated with the job.
        - `triggered_job_instances`: ManyToManyField linking to `TriggeredJobInstance` models representing the job's executions.
        - `trigger_source`: A field for specifying the source of the trigger (e.g., webhook URL).
        - `event_type`: The type of event that triggers the job.
        - `endpoint_url`: The URL endpoint that triggers the job, automatically generated based on the assistant and job ID.
        - `current_run_count`: Tracks the number of times the job has run.
        - `maximum_runs`: The maximum number of times the job is allowed to run.
        - `created_at`, `updated_at`: Timestamps for creation and last update.
        - `created_by_user`: ForeignKey linking to the `User` who created the job.
    - Methods:
        - `save()`: Overridden to generate the `endpoint_url` based on the assistant ID and job ID.
    - Meta:
        - `verbose_name`: "Triggered Job"
        - `verbose_name_plural`: "Triggered Jobs"
        - `ordering`: Orders jobs by creation date in descending order.
        - `indexes`: Indexes on various fields, including combinations of `name`, `trigger_assistant`, `created_by_user`, and `created_at` for optimized queries.
    """

    name = models.CharField(max_length=255)
    task_description = models.TextField(blank=True, null=True)
    step_guide = models.JSONField(default=list)

    trigger_assistant = models.ForeignKey('assistants.Assistant', on_delete=models.CASCADE,
                                          related_name='triggered_jobs')

    # TYPE: Trigger related fields
    trigger_source = models.CharField(max_length=2000, blank=True, null=True)
    event_type = models.CharField(max_length=4000, blank=True, null=True)
    endpoint_url = models.CharField(max_length=2000, blank=True, null=True)

    current_run_count = models.PositiveIntegerField(default=0)
    maximum_runs = models.PositiveIntegerField(default=1000)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='triggered_jobs')

    def __str__(self):
        return self.name + ' - ' + self.trigger_assistant.name + ' - ' + self.created_by_user.username + ' - ' + self.created_at.strftime(
            '%Y%m%d%H%M%S')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Triggered Job'
        verbose_name_plural = 'Triggered Jobs'
        indexes = [
            models.Index(fields=['name', 'trigger_assistant', 'created_by_user', 'created_at']),
            models.Index(fields=['created_at']),
            models.Index(fields=['trigger_assistant']),
            models.Index(fields=['created_by_user']),
            models.Index(fields=['trigger_assistant', 'created_by_user']),
            models.Index(fields=['trigger_assistant', 'created_by_user', 'created_at']),
            models.Index(fields=['trigger_assistant', 'created_by_user', 'created_at', 'name']),
            models.Index(fields=['trigger_assistant', 'created_by_user', 'created_at', 'name', 'current_run_count']),
        ]

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save(force_insert, force_update, using, update_fields)
        self.endpoint_url = BASE_URL + '/app/mm_triggered_jobs/api/v1/webhook/' + str(
            self.trigger_assistant.id) + '/' + str(self.id) + '/'
        super().save(force_insert, force_update, using, update_fields)
