#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: expert_network_reference_models.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:33
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


class ExpertNetworkAssistantReference(models.Model):
    network = models.ForeignKey("ExpertNetwork", on_delete=models.CASCADE, related_name='assistant_references')
    assistant = models.ForeignKey("assistants.Assistant", on_delete=models.CASCADE)
    context_instructions = models.TextField(default="", blank=True)
    created_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE,
                                        related_name='expert_network_assistant_references_created_by_user')
    last_updated_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE,
                                             related_name='expert_network_assistant_references_updated_by_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.network.name + " - " + self.assistant.name

    class Meta:
        verbose_name = "Expert Network Assistant Reference"
        verbose_name_plural = "Expert Network Assistant References"
        ordering = ["-created_at"]
        unique_together = [
            ["network", "assistant"],
        ]
        indexes = [
            models.Index(fields=["network"]),
            models.Index(fields=["assistant"]),
            models.Index(fields=["context_instructions"]),
            models.Index(fields=["created_by_user"]),
            models.Index(fields=["last_updated_by_user"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
            models.Index(fields=["network", "assistant"]),
            models.Index(fields=["network", "context_instructions"]),
            models.Index(fields=["network", "created_by_user"]),
            models.Index(fields=["network", "last_updated_by_user"]),
            models.Index(fields=["network", "created_at"]),
            models.Index(fields=["network", "updated_at"]),
            models.Index(fields=["assistant", "context_instructions"]),
            models.Index(fields=["assistant", "created_by_user"]),
            models.Index(fields=["assistant", "last_updated_by_user"]),
            models.Index(fields=["assistant", "created_at"]),
            models.Index(fields=["assistant", "updated_at"]),
            models.Index(fields=["created_by_user", "created_at"]),
            models.Index(fields=["created_by_user", "updated_at"]),
            models.Index(fields=["last_updated_by_user", "created_at"]),
            models.Index(fields=["last_updated_by_user", "updated_at"]),
            models.Index(fields=["network", "assistant", "context_instructions"]),
            models.Index(fields=["network", "assistant", "created_by_user"]),
            models.Index(fields=["network", "assistant", "last_updated_by_user"]),
            models.Index(fields=["network", "assistant", "created_at"]),
            models.Index(fields=["network", "assistant", "updated_at"]),
            models.Index(fields=["network", "context_instructions", "created_at"]),
            models.Index(fields=["network", "context_instructions", "updated_at"]),
            models.Index(fields=["network", "created_by_user", "created_at"]),
            models.Index(fields=["network", "created_by_user", "updated_at"]),
            models.Index(fields=["network", "last_updated_by_user", "created_at"]),
            models.Index(fields=["network", "last_updated_by_user", "updated_at"]),
            models.Index(fields=["assistant", "context_instructions", "created_at"]),
            models.Index(fields=["assistant", "context_instructions", "updated_at"]),
            models.Index(fields=["assistant", "created_by_user", "created_at"]),
            models.Index(fields=["assistant", "created_by_user", "updated_at"]),
            models.Index(fields=["assistant", "last_updated_by_user", "created_at"]),
            models.Index(fields=["assistant", "last_updated_by_user", "updated_at"]),
            models.Index(fields=["created_by_user", "created_at", "updated_at"]),
            models.Index(fields=["last_updated_by_user", "created_at", "updated_at"]),
        ]
