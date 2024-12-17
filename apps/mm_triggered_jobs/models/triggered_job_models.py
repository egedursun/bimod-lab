#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: triggered_job_models.py
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

from config.settings import BASE_URL


class TriggeredJob(models.Model):
    name = models.CharField(max_length=255)
    task_description = models.TextField(blank=True, null=True)
    step_guide = models.JSONField(default=list)

    trigger_assistant = models.ForeignKey(
        'assistants.Assistant',
        on_delete=models.CASCADE,
        related_name='triggered_jobs'
    )

    trigger_source = models.CharField(max_length=2000, blank=True, null=True)
    event_type = models.CharField(max_length=4000, blank=True, null=True)
    endpoint_url = models.CharField(max_length=2000, blank=True, null=True)

    current_run_count = models.PositiveIntegerField(default=0)
    maximum_runs = models.PositiveIntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by_user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='triggered_jobs'
    )

    def __str__(self):
        return self.name + ' - ' + self.trigger_assistant.name + ' - ' + self.created_by_user.username + ' - ' + self.created_at.strftime(
            '%Y%m%d%H%M%S')

    class Meta:
        ordering = ['-created_at']

        verbose_name = 'Triggered Job'
        verbose_name_plural = 'Triggered Jobs'

        unique_together = [
            [
                "trigger_assistant",
                "name"
            ],
        ]

        indexes = [
            models.Index(fields=[
                'name',
                'trigger_assistant',
                'created_by_user',
                'created_at'
            ]),
            models.Index(fields=[
                'created_at'
            ]),
            models.Index(fields=[
                'trigger_assistant'
            ]),
            models.Index(fields=[
                'created_by_user'
            ]),
            models.Index(fields=[
                'trigger_assistant',
                'created_by_user'
            ]),
            models.Index(fields=[
                'trigger_assistant',
                'created_by_user',
                'created_at'
            ]),
            models.Index(fields=[
                'trigger_assistant',
                'created_by_user',
                'created_at',
                'name'
            ]),
            models.Index(fields=[
                'trigger_assistant',
                'created_by_user',
                'created_at',
                'name',
                'current_run_count'
            ]),
        ]

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ):
        super().save(
            force_insert,
            force_update,
            using,
            update_fields
        )

        self.endpoint_url = BASE_URL + '/app/mm_triggered_jobs/api/v1/webhook/' + str(
            self.trigger_assistant.id
        ) + '/' + str(self.id) + '/'

        super().save(
            force_insert,
            force_update,
            using,
            update_fields
        )
