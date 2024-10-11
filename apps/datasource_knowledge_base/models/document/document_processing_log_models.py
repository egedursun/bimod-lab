#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: document_processing_log_models.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:47
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


class DocumentProcessingLog(models.Model):
    document_full_uri = models.CharField(max_length=1000)
    log_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.document_full_uri + " - " + self.created_at.strftime("%Y%m%d%H%M%S")

    class Meta:
        verbose_name = "Document Processing Log"
        verbose_name_plural = "Document Processing Logs"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["document_full_uri"]),
            models.Index(fields=["created_at"]),
        ]
