#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: request_log_models.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:44
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


class RequestLog(models.Model):
    export_assistant = models.ForeignKey('ExportAssistantAPI', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Request Log"
        verbose_name_plural = "Request Logs"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['export_assistant']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['export_assistant', 'timestamp']),
        ]
