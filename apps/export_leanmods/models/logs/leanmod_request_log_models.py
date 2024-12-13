#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: leanmod_request_log_models.py
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
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.db import models


class LeanmodRequestLog(models.Model):
    export_lean_assistant = models.ForeignKey(
        'ExportLeanmodAssistantAPI',
        on_delete=models.CASCADE
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Request LeanMod Log"
        verbose_name_plural = "Request LeanMod Logs"

        ordering = ['-timestamp']

        indexes = [
            models.Index(fields=[
                'export_lean_assistant'
            ]),
            models.Index(fields=[
                'timestamp'
            ]),
            models.Index(fields=[
                'export_lean_assistant',
                'timestamp'
            ]),
        ]
