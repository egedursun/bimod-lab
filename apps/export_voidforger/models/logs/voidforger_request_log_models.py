#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: orchestration_request_log_models.py
#  Last Modified: 2024-10-17 16:15:05
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-24 20:11:38
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


class VoidForgerRequestLog(models.Model):
    export_voidforger = models.ForeignKey(
        'ExportVoidForgerAPI',
        on_delete=models.CASCADE
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Request VoidForger Log"
        verbose_name_plural = "Request VoidForger Logs"

        ordering = ['-timestamp']

        indexes = [
            models.Index(fields=[
                'export_voidforger'
            ]),
            models.Index(fields=[
                'timestamp'
            ]),
            models.Index(fields=[
                'export_voidforger',
                'timestamp'
            ]),
        ]
