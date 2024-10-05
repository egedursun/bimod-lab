#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: orchestration_query_log_models.py
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

from apps.orchestrations.utils import ORCHESTRATION_QUERY_LOG_TYPES


class OrchestrationQueryLog(models.Model):
    orchestration_query = models.ForeignKey('orchestrations.OrchestrationQuery', on_delete=models.CASCADE,
                                            related_name='logs')
    log_type = models.CharField(max_length=100, choices=ORCHESTRATION_QUERY_LOG_TYPES, default="info")

    # Not always populated; only for worker assistant tool requests and responses
    context_worker = models.ForeignKey('assistants.Assistant', on_delete=models.SET_NULL, blank=True, null=True)

    log_text_content = models.TextField()
    log_image_contents = models.JSONField(default=list, blank=True, null=True)
    log_file_contents = models.JSONField(default=list, blank=True, null=True)
    log_audio_contents = models.JSONField(default=list, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.orchestration_query.query_text + " - " + self.orchestration_query.maestro.name + " - " + self.orchestration_query.maestro.organization.name

    class Meta:
        verbose_name = "Orchestration Query Log"
        verbose_name_plural = "Orchestration Query Logs"
        indexes = [
            # Single-field indexes
            models.Index(fields=["orchestration_query"]),
            models.Index(fields=["created_at"]),

            # Two-field composite indexes
            models.Index(fields=["orchestration_query", "created_at"]),
        ]
        unique_together = [["orchestration_query", "created_at"]]
