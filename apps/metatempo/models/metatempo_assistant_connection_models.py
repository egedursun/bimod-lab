#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: metatempo_assistant_connection_models.py
#  Last Modified: 2024-11-13 03:15:41
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-13 03:15:42
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


class MetaTempoAssistantConnection(models.Model):
    metatempo_instance = models.ForeignKey("metatempo.MetaTempoConnection", on_delete=models.CASCADE)
    assistant = models.ForeignKey("assistants.Assistant", on_delete=models.CASCADE)

    created_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.assistant} - {self.metatempo_instance}"

    class Meta:
        unique_together = ("metatempo_instance", "assistant")
        verbose_name = "Meta Tempo Assistant Connection"
        verbose_name_plural = "Meta Tempo Assistant Connections"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["metatempo_instance", "assistant"]),
            models.Index(fields=["assistant", "metatempo_instance"]),
        ]
