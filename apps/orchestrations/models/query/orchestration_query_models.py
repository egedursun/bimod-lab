#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: orchestration_query_models.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:41
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.db import models

from apps.orchestrations.models import Maestro


class OrchestrationQuery(models.Model):
    maestro = models.ForeignKey(Maestro, on_delete=models.CASCADE, related_name='queries')
    query_text = models.TextField()

    created_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE,
                                        related_name='orchestration_queries_created_by_user')
    last_updated_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE,
                                             related_name='orchestration_queries_last_updated_by_user')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.query_text + " - " + self.maestro.name + " - " + self.maestro.organization.name

    class Meta:
        verbose_name = "Orchestration Query"
        verbose_name_plural = "Orchestration Queries"
        indexes = [
            # Single-field indexes
            models.Index(fields=["maestro"]),
            models.Index(fields=["query_text"]),
            models.Index(fields=["created_by_user"]),
            models.Index(fields=["last_updated_by_user"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),

            # Two-field composite indexes
            models.Index(fields=["maestro", "query_text"]),
            models.Index(fields=["maestro", "created_by_user"]),
            models.Index(fields=["maestro", "last_updated_by_user"]),
            models.Index(fields=["maestro", "created_at"]),
            models.Index(fields=["maestro", "updated_at"]),
            models.Index(fields=["query_text", "created_at"]),
            models.Index(fields=["query_text", "updated_at"]),
            models.Index(fields=["created_by_user", "created_at"]),
            models.Index(fields=["created_by_user", "updated_at"]),
            models.Index(fields=["last_updated_by_user", "created_at"]),
            models.Index(fields=["last_updated_by_user", "updated_at"]),

            # Three-field composite indexes
            models.Index(fields=["maestro", "query_text", "created_at"]),
            models.Index(fields=["maestro", "query_text", "updated_at"]),
            models.Index(fields=["maestro", "created_by_user", "created_at"]),
            models.Index(fields=["maestro", "created_by_user", "updated_at"]),
            models.Index(fields=["maestro", "last_updated_by_user", "created_at"]),
            models.Index(fields=["maestro", "last_updated_by_user", "updated_at"]),
            models.Index(fields=["query_text", "created_at", "updated_at"]),
            models.Index(fields=["created_by_user", "created_at", "updated_at"]),
            models.Index(fields=["last_updated_by_user", "created_at", "updated_at"]),

            # Four-field composite indexes
            models.Index(fields=["maestro", "query_text", "created_at", "updated_at"]),
            models.Index(fields=["maestro", "created_by_user", "created_at", "updated_at"]),
            models.Index(fields=["maestro", "last_updated_by_user", "created_at", "updated_at"]),
        ]
