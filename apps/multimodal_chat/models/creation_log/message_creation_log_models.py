#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: message_creation_log_models.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:41
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
#  File: message_creation_log_models.py
#  Last Modified: 2024-09-28 20:38:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:05:24
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

#
from django.db import models


# NOTE: Counts both the Normal Chat Messages and Lean Chat Messages
class ChatMessageCreationLog(models.Model):
    """
    ChatMessageCreationLog Model:
    - Purpose: Represents a log entry for the creation of a message within a multimodal chat. It stores the organization associated with the message and the timestamp of creation.
    - Key Fields:
        - `organization`: ForeignKey linking to the `Organization` model.
        - `created_at`: Timestamp for when the message was created.
    - Meta:
        - `verbose_name`: "Chat Message Creation Log"
        - `verbose_name_plural`: "Chat Message Creation Logs"
        - `ordering`: Orders logs by creation date in descending order.
        - `indexes`: Indexes on the creation date for optimized queries.
    """

    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at}"

    class Meta:
        verbose_name = "Chat Message Creation Log"
        verbose_name_plural = "Chat Message Creation Logs"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['created_at']),
        ]
