#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: request_log_models.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:42
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: request_log_models.py
#  Last Modified: 2024-09-27 19:45:58
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:50:16
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.db import models


class RequestLog(models.Model):
    """
    RequestLog Model:
    - Purpose: Tracks individual API requests made to an exported assistant API, storing the timestamp and linking each request to the corresponding `ExportAssistantAPI`.
    - Key Fields:
        - `export_assistant`: ForeignKey linking to the `ExportAssistantAPI` model.
        - `timestamp`: The timestamp of when the API request was made.
    - Meta:
        - `verbose_name`: "Request Log"
        - `verbose_name_plural`: "Request Logs"
        - `ordering`: Orders logs by timestamp in descending order.
        - `indexes`: Indexes on `export_assistant`, `timestamp`, and their combination for optimized queries.
    """

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
