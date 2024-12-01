#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: meta_kanban_assistant_connection_models.py
#  Last Modified: 2024-11-13 02:45:42
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-13 02:45:43
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


class MetaKanbanAssistantConnection(models.Model):
    metakanban_board = models.ForeignKey("MetaKanbanBoard", on_delete=models.CASCADE)
    assistant = models.ForeignKey("assistants.Assistant", on_delete=models.CASCADE)

    created_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.assistant} - {self.metakanban_board}"

    class Meta:
        unique_together = [
            ["metakanban_board", "assistant"],
        ]
        verbose_name = "Meta Kanban Assistant Connection"
        verbose_name_plural = "Meta Kanban Assistant Connections"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["metakanban_board", "assistant"]),
            models.Index(fields=["assistant", "metakanban_board"]),
        ]
