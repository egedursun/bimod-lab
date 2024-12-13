#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: export_orchestration_models.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:46
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
from django.utils import timezone

from apps.export_orchestrations.utils import (
    generate_orchestration_endpoint,
    generate_orchestration_custom_api_key
)

from config.settings import (
    BASE_URL,
    EXPORT_ORCHESTRATION_API_BASE_URL
)


class ExportOrchestrationAPI(models.Model):
    organization = models.ForeignKey(
        "organization.Organization",
        on_delete=models.CASCADE,
        related_name='exported_orchestrations',
        null=True,
        blank=True
    )

    orchestrator = models.ForeignKey(
        'orchestrations.Maestro',
        on_delete=models.CASCADE,
        related_name='exported_orchestrations'
    )

    is_public = models.BooleanField(default=False)
    request_limit_per_hour = models.IntegerField(default=1000)
    is_online = models.BooleanField(default=True)

    custom_api_key = models.CharField(
        max_length=1000,
        blank=True,
        null=True,
        unique=True
    )

    endpoint = models.CharField(
        max_length=1000,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by_user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name='export_orchestrations_created_by_user'
    )

    def __str__(self):
        return self.orchestrator.name

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ):
        super().save(force_insert, force_update, using, update_fields)

        if not self.endpoint:
            self.endpoint = BASE_URL + "/" + EXPORT_ORCHESTRATION_API_BASE_URL + "/" + generate_orchestration_endpoint(
                self.orchestrator, self.id)

            self.save()

        if not self.custom_api_key and (not self.is_public):
            self.custom_api_key = generate_orchestration_custom_api_key(
                self.orchestrator
            )

            self.save()

    def requests_in_last_hour(self):
        from apps.export_orchestrations.models import OrchestratorRequestLog

        one_hour_ago = timezone.now() - timezone.timedelta(hours=1)

        return OrchestratorRequestLog.objects.filter(
            export_orchestration=self,
            timestamp__gte=one_hour_ago
        ).count()

    def requests_limit_reached(self):
        return self.requests_in_last_hour() >= self.request_limit_per_hour

    class Meta:
        verbose_name = "Export Orchestration API"
        verbose_name_plural = "Export Orchestration APIs"
        ordering = ['-created_at']

        unique_together = [
            [
                'organization',
                'orchestrator',
                'is_public'
            ],
        ]

        indexes = [
            models.Index(fields=[
                'orchestrator'
            ]),
            models.Index(fields=[
                'created_by_user'
            ]),
            models.Index(fields=[
                'created_at'
            ]),
            models.Index(fields=[
                'updated_at'
            ]),
            models.Index(fields=[
                'orchestrator',
                'created_at'
            ]),
            models.Index(fields=[
                'orchestrator',
                'updated_at'
            ]),
            models.Index(fields=[
                'orchestrator',
                'created_by_user'
            ]),
        ]
