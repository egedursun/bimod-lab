#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: beamguard_artifact_models.py
#  Last Modified: 2024-12-02 01:23:29
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-02 01:23:29
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

from apps.beamguard.utils import (
    BEAMGUARD_ARTIFACT_TYPES,
    BeamGuardArtifactTypesNames,
    BeamGuardConfirmationStatusesNames,
    BEAMGUARD_CONFIRMATION_STATUSES,
)


class BeamGuardArtifact(models.Model):
    assistant = models.ForeignKey(
        'assistants.Assistant',
        on_delete=models.CASCADE,
        related_name='beamguard_artifacts',
        null=True,
        blank=True
    )
    chat = models.ForeignKey(
        'multimodal_chat.MultimodalChat',
        on_delete=models.CASCADE,
        related_name='beamguard_artifacts',
        null=True,
        blank=True
    )

    name = models.CharField(max_length=10000, null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)

    confirmation_status = models.CharField(
        max_length=500,
        choices=BEAMGUARD_CONFIRMATION_STATUSES,
        default=BeamGuardConfirmationStatusesNames.PENDING
    )

    type = models.CharField(max_length=500, choices=BEAMGUARD_ARTIFACT_TYPES)
    raw_query = models.TextField(null=True, blank=True)

    sql_connection_object = models.ForeignKey(
        'datasource_sql.SQLDatabaseConnection',
        on_delete=models.CASCADE,
        related_name='beamguard_artifacts',
        default=None,
        null=True,
        blank=True,
    )
    nosql_connection_object = models.ForeignKey(
        'datasource_nosql.NoSQLDatabaseConnection',
        on_delete=models.CASCADE,
        related_name='beamguard_artifacts',
        default=None,
        null=True,
        blank=True,
    )
    file_system_connection_object = models.ForeignKey(
        'datasource_file_systems.DataSourceFileSystem',
        on_delete=models.CASCADE,
        related_name='beamguard_artifacts',
        default=None,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'BeamGuard Artifacts'
        verbose_name = 'BeamGuard Artifact'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['assistant', 'type']),
            models.Index(fields=['assistant', 'type', 'created_at']),
            models.Index(fields=['assistant', 'type', 'created_at', 'name']),
        ]

    def __str__(self):
        return f"{self.assistant.name} - {self.type} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

    def save(self, *args, **kwargs):

        if self.type == BeamGuardArtifactTypesNames.SQL and self.sql_connection_object is None:
            raise ValueError("SQL Connection Object is required for SQL BeamGuard Artifact.")

        if self.type == BeamGuardArtifactTypesNames.NOSQL and self.nosql_connection_object is None:
            raise ValueError("NoSQL Connection Object is required for NoSQL BeamGuard Artifact.")

        if self.type == BeamGuardArtifactTypesNames.FILE_SYSTEM and self.file_system_connection_object is None:
            raise ValueError("File System Connection Object is required for File System BeamGuard Artifact.")

        super().save(*args, **kwargs)
