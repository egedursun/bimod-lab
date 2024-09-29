#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: orchestration_request_log_models.py
#  Last Modified: 2024-09-28 15:08:41
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:52:27
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.db import models


class OrchestratorRequestLog(models.Model):
    export_orchestration = models.ForeignKey('ExportOrchestrationAPI', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Request Orchestration Log"
        verbose_name_plural = "Request Orchestration Logs"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['export_orchestration']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['export_orchestration', 'timestamp']),
        ]
