#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: beamguard_artifact_admin.py
#  Last Modified: 2024-12-02 01:23:40
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-02 01:23:40
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

"""
class BeamGuardArtifact(models.Model):
    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE,
        related_name='beamguard_artifacts'
    )

    nickname = models.CharField(max_length=10000, null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)

    type = models.CharField(max_length=500, choices=BEAMGUARD_ARTIFACT_TYPES)
    sql_connection_object = models.ForeignKey(
        'datasource_sql.SQLDatabaseConnection',
        on_delete=models.CASCADE,
        related_name='beamguard_artifacts',
        default=None,
        null=True
    )
    nosql_connection_object = models.ForeignKey(
        'datasource_nosql.NoSQLDatabaseConnection',
        on_delete=models.CASCADE,
        related_name='beamguard_artifacts',
        default=None,
        null=True
    )
    file_system_connection_object = models.ForeignKey(
        'datasource_file_systems.DataSourceFileSystem',
        on_delete=models.CASCADE,
        related_name='beamguard_artifacts',
        default=None,
        null=True
    )

    created_by_assistant = models.ForeignKey(
        'assistants.Assistant',
        on_delete=models.CASCADE,
        related_name='beamguard_artifacts',
        default=None,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'BeamGuard Artifacts'
        verbose_name = 'BeamGuard Artifact'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['organization', 'type']),
            models.Index(fields=['organization', 'type', 'created_at']),
            models.Index(fields=['organization', 'type', 'created_at', 'nickname']),
        ]

    def __str__(self):
        return f"{self.organization.name} - {self.type} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

    def save(self, *args, **kwargs):

        if self.type == BeamGuardArtifactTypesNames.SQL and self.sql_connection_object is None:
            raise ValueError("SQL Connection Object is required for SQL BeamGuard Artifact.")

        if self.type == BeamGuardArtifactTypesNames.NOSQL and self.nosql_connection_object is None:
            raise ValueError("NoSQL Connection Object is required for NoSQL BeamGuard Artifact.")

        if self.type == BeamGuardArtifactTypesNames.FILE_SYSTEM and self.file_system_connection_object is None:
            raise ValueError("File System Connection Object is required for File System BeamGuard Artifact.")

        super().save(*args, **kwargs)

"""

from django.contrib import admin

from apps.beamguard.models import BeamGuardArtifact

from apps.beamguard.utils import (
    BEAMGUARD_ARTIFACT_ADMIN_LIST,
    BEAMGUARD_ARTIFACT_ADMIN_SEARCH,
    BEAMGUARD_ARTIFACT_ADMIN_FILTER,
)


@admin.register(BeamGuardArtifact)
class BeamGuardArtifactAdmin(admin.ModelAdmin):
    list_display = BEAMGUARD_ARTIFACT_ADMIN_LIST
    search_fields = BEAMGUARD_ARTIFACT_ADMIN_SEARCH
    list_filter = BEAMGUARD_ARTIFACT_ADMIN_FILTER
    ordering = ('-created_at',)
