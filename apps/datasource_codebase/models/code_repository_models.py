#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: code_repository_models.py
#  Last Modified: 2024-10-05 01:39:47
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

import logging

from django.db import models
from slugify import slugify

logger = logging.getLogger(__name__)


class CodeBaseRepository(models.Model):
    knowledge_base = models.ForeignKey(
        "CodeRepositoryStorageConnection",
        on_delete=models.CASCADE,
        related_name="code_base_repositories"
    )

    repository_uri = models.CharField(
        max_length=1000,
        null=True,
        blank=True
    )

    repository_name = models.CharField(max_length=1000)
    repository_description = models.TextField()

    n_chunks_indexed_status = models.IntegerField(default=0)
    n_chunks = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by_user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='created_code_base_repositories',
        null=True,
        blank=True,
    )

    def __str__(self):
        return slugify(self.repository_name) + " - " + self.knowledge_base.name + " - " + self.created_at.strftime(
            "%Y%m%d%H%M%S")

    class Meta:
        verbose_name = "Code Base Repository"
        verbose_name_plural = "Code Base Repositories"

        unique_together = [
            [
                "knowledge_base",
                "repository_uri"
            ],
        ]

        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=[
                "knowledge_base",
                "repository_name"
            ]),
            models.Index(fields=[
                "knowledge_base",
                "created_at"
            ]),
            models.Index(fields=[
                "knowledge_base",
                "updated_at"
            ]),
        ]
