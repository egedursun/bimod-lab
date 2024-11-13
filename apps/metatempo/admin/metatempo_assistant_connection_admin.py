#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: metatempo_assistant_connection_admin.py
#  Last Modified: 2024-11-13 03:17:17
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-13 03:17:17
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


"""
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

"""

from django.contrib import admin

from apps.metatempo.models import MetaTempoAssistantConnection
from apps.metatempo.utils import METATEMPO_ASSISTANT_CONNECTION_ADMIN_LIST, \
    METATEMPO_ASSISTANT_CONNECTION_ADMIN_FILTER, METATEMPO_ASSISTANT_CONNECTION_ADMIN_SEARCH


@admin.register(MetaTempoAssistantConnection)
class MetaTempoAssistantConnectionAdmin(admin.ModelAdmin):
    list_display = METATEMPO_ASSISTANT_CONNECTION_ADMIN_LIST
    list_filter = METATEMPO_ASSISTANT_CONNECTION_ADMIN_FILTER
    search_fields = METATEMPO_ASSISTANT_CONNECTION_ADMIN_SEARCH
    ordering = ["-created_at"]
